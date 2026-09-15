#!/usr/bin/env python3
"""
gg_insights_generator.py — Reads real system data, generates structured insights.
Runs every 30min as part of sync pipeline. No LLM — pure data analysis.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
from task_hub import pg_cursor

HKT = timezone(timedelta(hours=8))

def hkt_now():
    return datetime.now(HKT)

def clear_old_insights():
    """Keep only last 48h of insights."""
    with pg_cursor(commit=True) as cur:
        cur.execute("DELETE FROM gg_insights WHERE created_at < %s",
                    (hkt_now() - timedelta(hours=48),))
        return cur.rowcount

def add_insight(cat, source, title, content, priority="medium", meta=None):
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO gg_insights (category, source, title, content, priority, metadata, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cat, source, title, content, priority,
              json.dumps(meta) if meta else None, hkt_now()))

# ═══ 1. GG VOICES — each AI's perspective based on actual data ═══

def gen_voices():
    """Generate what each AI would say based on real system data."""
    now = hkt_now()

    # --- Fighter voice ---
    with pg_cursor() as cur:
        cur.execute("SELECT status, message, synced_at FROM sync_status ORDER BY synced_at DESC")
        syncs = cur.fetchall()
        
        # Find any failed syncs
        failed_syncs = [s for s in syncs if s["status"] == "error"]
        if failed_syncs:
            add_insight("voice", "fighter",
                "⚠️ Sync issues need attention",
                f"{len(failed_syncs)} sync source(s) failing: " +
                ", ".join(f"{s['source']}: {s['message']}" for s in failed_syncs[:3]),
                "high", {"component": "sync"})

    # Recent task completion rate
    with pg_cursor() as cur:
        cur.execute("""
            SELECT action, COUNT(*) as cnt
            FROM task_audit
            WHERE changed_at >= %s
            GROUP BY action ORDER BY cnt DESC
        """, (now - timedelta(hours=24),))
        actions = {r["action"]: r["cnt"] for r in cur.fetchall()}
        completed = actions.get("completed", 0)
        created = actions.get("created", 0)
        if completed > 0 or created > 0:
            add_insight("voice", "fighter",
                f"📊 Today: {completed} tasks done, {created} new",
                f"Completion rate: {completed}/{created if created else 1} in 24h. " +
                ("Good pace! Keeping up." if completed >= created * 0.5
                 else "Room to improve — some tasks are lingering."),
                "medium", {"actions": actions})

    # --- Work voice — MCP health ---
    with pg_cursor() as cur:
        cur.execute("""
            SELECT name, status, error, last_check FROM connection_status
            WHERE status = 'failed' ORDER BY last_check DESC
        """)
        failed_mcps = cur.fetchall()
        if failed_mcps:
            names = [f["name"] for f in failed_mcps[:3]]
            add_insight("voice", "work",
                f"🔴 {len(failed_mcps)} MCP server(s) down",
                f"Failing: {', '.join(names)}. These need attention — "
                "some may have stale binary paths or missing configs.",
                "high", {"failed": [{
                    "name": f["name"],
                    "status": f["status"],
                    "error": f["error"],
                    "last_check": f["last_check"].isoformat() if f.get("last_check") else ""
                } for f in failed_mcps]})
        else:
            add_insight("voice", "work",
                "✅ All MCP servers healthy",
                f"All {len(failed_mcps) if 'failed_mcps' in dir() else 0} MCP endpoints responding.",
                "low")

    # --- Person voice — task patterns ---
    with pg_cursor() as cur:
        cur.execute("""
            SELECT notion_page_id, title, action, changed_at
            FROM task_audit
            WHERE changed_at >= %s AND action = 'created'
            ORDER BY changed_at DESC LIMIT 3
        """, (now - timedelta(hours=48),))
        recent = cur.fetchall()
        if recent:
            titles = [r["title"][:30] for r in recent]
            add_insight("voice", "person",
                "📋 New tasks spotted",
                f"Recently added: {', '.join(titles)}. "
                "Making sure nothing falls through the cracks.",
                "medium", {"recent": [dict(r) for r in recent]})

# ═══ 2. DISCOVERIES — system observations based on data ═══

def gen_discoveries():
    with pg_cursor() as cur:
        cur.execute("""
            SELECT ai_name, COUNT(*) as cnt,
                   AVG(cpu) as avg_cpu, AVG(mem) as avg_mem,
                   MAX(recorded_at) as latest
            FROM ai_snapshot
            WHERE recorded_at >= %s
            GROUP BY ai_name
        """, (hkt_now() - timedelta(hours=24),))
        ai_stats = cur.fetchall()
        for s in ai_stats:
            avg_cpu = round(float(s["avg_cpu"] or 0), 1)
            avg_mem = round(float(s["avg_mem"] or 0), 1)
            name = s["ai_name"]
            label = {"fighter": "🔥 Fighter", "work": "⚙️ Work", "person": "❤️ Person"}.get(name, name)
            status = "stable" if avg_cpu < 20 else "busy"
            add_insight("discovery", "system",
                f"{label}: {status} (CPU {avg_cpu}%, MEM {avg_mem}%)",
                f"24h avg. {s['cnt']} data points. "
                f"{'Normal load, plenty of headroom.' if avg_cpu < 20 else 'Moderate activity.'}",
                "low", {"ai": name, "avg_cpu": avg_cpu, "avg_mem": avg_mem, "points": s["cnt"]})

# ═══ 3. UPGRADE SUGGESTIONS — based on gaps in current system ═══

def gen_suggestions():
    with pg_cursor() as cur:
        # Check if we have sync_status data
        cur.execute("SELECT COUNT(*) as cnt FROM sync_status")
        sync_count = dict(cur.fetchone())["cnt"]
        if sync_count == 0:
            add_insight("suggestion", "system",
                "💡 Enable sync logging to track system health",
                "sync_status table is empty — no data sources are tracking their sync status. "
                "This makes it hard to know if background jobs are actually running.",
                "medium")

        # Check task_audit
        cur.execute("SELECT COUNT(*) as cnt FROM task_audit")
        audit_count = dict(cur.fetchone())["cnt"]
        if audit_count > 0:
            add_insight("suggestion", "system",
                f"📈 Task audit trail active: {audit_count} entries",
                f"Task change tracking is working with {audit_count} entries. "
                "Could add a weekly trend view to show productivity patterns.",
                "low", {"audit_count": audit_count})

# ═══ MAIN ═══

def main():
    now = hkt_now()
    print(f"[gg_insights] Generating @ {now.strftime('%H:%M')}")

    cleared = clear_old_insights()
    print(f"  Cleared {cleared} old insights")

    gen_voices()
    print("  Voices generated")

    gen_discoveries()
    print("  Discoveries generated")

    gen_suggestions()
    print("  Suggestions generated")

    # Update sync_status
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO sync_status (source, status, message, rows_synced, synced_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source) DO UPDATE SET
                status=%s, message=%s, rows_synced=%s, synced_at=%s
        """, ("gg_insights", "ok", "insights generated", 0, now,
              "ok", "insights generated", 0, now))

    print("[gg_insights] Done")
    return 0

if __name__ == "__main__":
    sys.exit(main())
