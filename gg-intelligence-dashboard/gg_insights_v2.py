#!/usr/bin/env python3
"""
gg_insights_v2.py — Deep system analysis → structured insights with drill-down data.
Stores insights + detail payloads in gg_insights table. Zero LLM.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
from collections import defaultdict
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
from task_hub import pg_cursor

HKT = timezone(timedelta(hours=8))

def hkt_now():
    return datetime.now(HKT)

def fmt(ts):
    return ts.isoformat() if ts else ""

def add_insight(cat, source, title, content, priority="medium", detail=None):
    """Insert an insight with optional detail JSON (for click-to-expand)."""
    now = hkt_now()
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO gg_insights (category, source, title, content, priority, metadata, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cat, source, title, content, priority,
              json.dumps(detail) if detail else None, now))

def clear_old(keep_hours=48):
    """Delete old insights, keeping only recent ones from data-fact generator."""
    with pg_cursor(commit=True) as cur:
        # Delete v2 data-fact insights that are older, plus clear old LLM thoughts
        cur.execute("""
            DELETE FROM gg_insights
            WHERE (category != 'voice' AND created_at < %s)
               OR (category = 'voice' AND created_at < %s)
        """, (hkt_now() - timedelta(hours=6), hkt_now() - timedelta(hours=48)))
        return cur.rowcount

# ═══════════════════════════════════════════
# ANALYSIS FUNCTIONS — each returns (insights_list)
# Each insight: {title, content, priority, source, detail: {...}}
# ═══════════════════════════════════════════

def analyze_mcp_trends():
    """Cross-reference connection_status with itself to find changes."""
    insights = []
    now = hkt_now()
    day_ago = now - timedelta(hours=24)
    with pg_cursor() as cur:
        # Endpoints that changed status in last 24h
        cur.execute("""
            SELECT name, status, last_ok, last_fail, last_check, error
            FROM connection_status
            ORDER BY name
        """)
        all_eps = cur.fetchall()

        for ep in all_eps:
            n, st, lok, lfa, lch, err = ep["name"], ep["status"], ep["last_ok"], ep["last_fail"], ep["last_check"], ep["error"]
            if st == "failed" and lfa and lfa >= day_ago:
                detail = {
                    "endpoint": n,
                    "status": st,
                    "error": err,
                    "last_fail": fmt(lfa),
                    "last_check": fmt(lch),
                    "last_ok": fmt(lok),
                    "duration_min": int((now - lfa.replace(tzinfo=HKT)).total_seconds() / 60) if lfa else 0,
                    "suggested_action": "Check binary path or config.yaml entry" if "not found" in (err or "") else "Restart MCP server"
                }
                insights.append({
                    "title": f"🔴 {n} — down {detail['duration_min']}m",
                    "content": f"{err}. Last worked: {fmt(lok) if lok else 'never'}.",
                    "priority": "high", "source": "work",
                    "detail": detail
                })
            elif st == "connected" and lok and lok >= day_ago:
                pass  # Healthy — skip for noise reduction

    return insights


def analyze_task_velocity():
    """Task completion patterns — velocity, bottlenecks, stale tasks."""
    insights = []
    now = hkt_now()
    week_ago = now - timedelta(days=7)
    day_ago = now - timedelta(hours=24)

    with pg_cursor() as cur:
        # Completions by day (last 7 days)
        cur.execute("""
            SELECT DATE(changed_at AT TIME ZONE 'Asia/Hong_Kong') as day, COUNT(*) as cnt
            FROM task_audit WHERE action IN ('completed') AND changed_at >= %s
            GROUP BY day ORDER BY day
        """, (week_ago,))
        daily = cur.fetchall()

        if len(daily) >= 2:
            total = sum(r["cnt"] for r in daily)
            avg = total / len(daily)
            # Trend: is today above or below average?
            today = now.strftime("%Y-%m-%d")
            today_tasks = sum(r["cnt"] for r in daily if str(r["day"]) == today)

            trend = "faster" if today_tasks > avg else "slower"
            detail = {
                "daily_counts": {str(r["day"]): r["cnt"] for r in daily},
                "avg_per_day": round(avg, 1),
                "total_7d": total,
                "today": today_tasks,
                "trend": trend
            }
            p = "low" if today_tasks >= avg else "medium"
            insights.append({
                "title": f"📊 Task velocity: {trend} than average",
                "content": f"{today_tasks} done today vs {round(avg,1)}/day avg (7d: {total}). "
                           f"{'🔥 Keep the momentum!' if trend == 'faster' else '📉 Could pick up — {round(avg - today_tasks,1)} behind pace.'}",
                "priority": p, "source": "fighter",
                "detail": detail
            })

        # Stale tasks — created but no completion in 7+ days
        cur.execute("""
            SELECT DISTINCT ON (t.notion_page_id) t.notion_page_id, t.title, t.status,
                   a.changed_at as last_change, t.created_at
            FROM tasks t
            LEFT JOIN task_audit a ON a.notion_page_id = t.notion_page_id
            WHERE t.status NOT IN ('done', 'cancelled')
              AND (a.changed_at IS NULL OR a.changed_at < %s)
            ORDER BY t.notion_page_id, a.changed_at DESC NULLS LAST
            LIMIT 5
        """, (day_ago,))
        stale = cur.fetchall()
        if stale:
            detail = {
                "stale_tasks": [{
                    "title": s["title"], "status": s["status"],
                    "last_change": fmt(s["last_change"]),
                    "created": fmt(s["created_at"])
                } for s in stale]
            }
            insights.append({
                "title": f"🧹 {len(stale)} stale tasks — no activity in 24h+",
                "content": f"Tasks like \"{stale[0]['title'][:30]}...\" haven't been touched. "
                           f"Consider reviewing or bumping priority.",
                "priority": "medium", "source": "person",
                "detail": detail
            })

    return insights


def analyze_ai_health_trends():
    """AI health trends — CPU trend, mem trend, uptime comparison."""
    insights = []
    now = hkt_now()
    day_ago = now - timedelta(hours=24)
    two_days = now - timedelta(hours=48)

    with pg_cursor() as cur:
        for ai in ["fighter", "work", "person"]:
            # Compare last 24h CPU vs previous 24h
            cur.execute("""
                SELECT AVG(cpu) as avg_cpu, MAX(cpu) as max_cpu, MIN(cpu) as min_cpu,
                       COUNT(*) as samples
                FROM ai_snapshot
                WHERE ai_name = %s AND recorded_at >= %s
            """, (ai, day_ago))
            recent = cur.fetchone()

            cur.execute("""
                SELECT AVG(cpu) as avg_cpu_prev
                FROM ai_snapshot
                WHERE ai_name = %s AND recorded_at >= %s AND recorded_at < %s
            """, (ai, two_days, day_ago))
            prev = cur.fetchone()

            if not recent or not recent["avg_cpu"]:
                continue

            avg_cpu = round(float(recent["avg_cpu"]), 1)
            max_cpu = round(float(recent["max_cpu"]), 1)
            prev_avg = round(float(prev["avg_cpu_prev"] or 0), 1) if prev and prev.get("avg_cpu_prev") else None

            label = {"fighter": "🔥 Fighter", "work": "⚙️ Work", "person": "❤️ Person"}.get(ai, ai)

            if prev_avg and abs(avg_cpu - prev_avg) > 5:
                direction = "up" if avg_cpu > prev_avg else "down"
                insights.append({
                    "title": f"📈 {label} CPU {direction} {abs(avg_cpu - prev_avg)}%",
                    "content": f"24h avg: {avg_cpu}% (prev: {prev_avg}%). Peak: {max_cpu}%. "
                               f"{'Possible increased load.' if direction == 'up' else 'Recovered from previous load.'}",
                    "priority": "medium" if direction == "up" else "low",
                    "source": "system",
                    "detail": {
                        "ai": ai, "avg_cpu": avg_cpu, "max_cpu": max_cpu,
                        "prev_avg_cpu": prev_avg, "direction": direction,
                        "samples": recent["samples"]
                    }
                })
            elif max_cpu > 50:
                insights.append({
                    "title": f"⚠️ {label} hit {max_cpu}% CPU peak",
                    "content": f"24h avg: {avg_cpu}%. That peak might be a heavy cron or sync job.",
                    "priority": "low", "source": "system",
                    "detail": {
                        "ai": ai, "avg_cpu": avg_cpu, "max_cpu": max_cpu,
                        "min_cpu": round(float(recent["min_cpu"] or 0), 1) if recent.get("min_cpu") else 0
                    }
                })

    return insights


def analyze_sync_health():
    """Sync status — latency, failures, gaps."""
    insights = []
    now = hkt_now()
    day_ago = now - timedelta(hours=24)

    with pg_cursor() as cur:
        cur.execute("""
            SELECT source, status, message, synced_at
            FROM sync_status
            ORDER BY synced_at DESC
        """)
        syncs = cur.fetchall()

        for s in syncs:
            src = s["source"]
            if s["status"] == "error":
                delay = int((now - s["synced_at"].replace(tzinfo=HKT)).total_seconds() / 60) if s.get("synced_at") else 0
                insights.append({
                    "title": f"❌ {src} sync failing ({delay}m ago)",
                    "content": f"{s['message']}. Last attempted {delay} min ago.",
                    "priority": "high", "source": "work",
                    "detail": {
                        "source": src, "error": s["message"],
                        "last_attempt": fmt(s["synced_at"]), "delay_min": delay
                    }
                })

        # Check for stale syncs (no update >30min)
        for s in syncs:
            src = s["source"]
            if not s.get("synced_at") or s["status"] == "error":
                continue
            delay = int((now - s["synced_at"].replace(tzinfo=HKT)).total_seconds() / 60)
            if delay > 30 and src not in ("gg_insights",):  # insights only runs every 15min
                insights.append({
                    "title": f"⏰ {src} sync overdue ({delay}m since last)",
                    "content": f"Expected every 15min. Last sync was {delay} min ago. Possible cron issue.",
                    "priority": "medium", "source": "work",
                    "detail": {
                        "source": src, "delay_min": delay,
                        "last_sync": fmt(s["synced_at"]),
                        "expected_interval": "15min"
                    }
                })

    return insights


def analyze_project_distribution():
    """Task distribution by project/area."""
    insights = []
    with pg_cursor() as cur:
        cur.execute("""
            SELECT project, COUNT(*) as cnt
            FROM tasks
            WHERE status NOT IN ('done', 'cancelled') AND project IS NOT NULL
            GROUP BY project ORDER BY cnt DESC
            LIMIT 5
        """)
        projects = cur.fetchall()
        if projects:
            total = sum(r["cnt"] for r in projects)
            detail = {r["project"]: r["cnt"] for r in projects}
            top = projects[0]
            pct = round(top["cnt"] / total * 100) if total else 0
            insights.append({
                "title": f"📋 Most tasks in: {top['project'][:20]} ({pct}%)",
                "content": f"{total} active tasks across {len(projects)} project areas. "
                           f"Top: {top['project'][:20]} ({top['cnt']}), "
                           f"followed by {projects[1]['project'][:15] if len(projects)>1 else '—'}.",
                "priority": "low", "source": "person",
                "detail": {"projects": detail, "total": total}
            })

    return insights


def analyze_cron_reliability():
    """Read recent cron error logs for patterns."""
    insights = []
    cron_log = "/tmp/ai_results/results.jsonl"
    if not os.path.exists(cron_log):
        return insights

    try:
        with open(cron_log) as f:
            lines = f.readlines()[-100:]
        errors = [json.loads(l) for l in lines if "error" in l.lower() or "fail" in l.lower()]
        if errors:
            jobs = set(e.get("job", "?") for e in errors)
            insights.append({
                "title": f"⚠️ {len(errors)} cron errors in recent log",
                "content": f"Affected jobs: {', '.join(jobs)}. Check cron doctor for details.",
                "priority": "medium", "source": "system",
                "detail": {"error_count": len(errors), "jobs": list(jobs)}
            })
    except:
        pass

    return insights


# ═══ MAIN ═══

def main():
    now = hkt_now()
    print(f"[gg_insights v2] @ {now.strftime('%H:%M')}")

    cleared = clear_old(48)
    print(f"  Cleared {cleared} old entries")

    all_insights = []
    all_insights += analyze_mcp_trends()
    all_insights += analyze_task_velocity()
    all_insights += analyze_ai_health_trends()
    all_insights += analyze_sync_health()
    all_insights += analyze_project_distribution()
    all_insights += analyze_cron_reliability()

    for ins in all_insights:
        add_insight(
            cat=ins.get("cat", 
                "voice" if ins["source"] in ("fighter","work","person") else 
                "discovery" if "CPU" in ins["title"] or "trend" in ins["title"] or "distribution" in ins["title"] else
                "suggestion" if "sync" in ins["title"].lower() or "stale" in ins["title"].lower() else
                "discovery"),
            source=ins["source"],
            title=ins["title"],
            content=ins["content"],
            priority=ins["priority"],
            detail=ins.get("detail")
        )

    print(f"  Generated {len(all_insights)} insights")

    with pg_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO sync_status (source, status, message, rows_synced, synced_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source) DO UPDATE SET
                status=%s, message=%s, rows_synced=%s, synced_at=%s
        """, ("gg_insights", "ok", f"{len(all_insights)} insights", len(all_insights), now,
              "ok", f"{len(all_insights)} insights", len(all_insights), now))

    print("[gg_insights v2] Done")
    return 0

if __name__ == "__main__":
    sys.exit(main())
