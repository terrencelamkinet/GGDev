#!/usr/bin/env python3
"""gg_context.py — Collects system context into a JSON file for LLM consumption."""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
from task_hub import pg_cursor

HKT = timezone(timedelta(hours=8))
OUTPUT = "/tmp/gg_system_context.json"

def hkt_now():
    return datetime.now(HKT)

def fmt(ts):
    return ts.isoformat() if ts else ""

def collect():
    ctx = {"generated_at": hkt_now().isoformat()}

    with pg_cursor() as cur:
        # MCP status
        cur.execute("SELECT name, status, error, category FROM connection_status ORDER BY name")
        ctx["mcps"] = [dict(r) for r in cur.fetchall()]

        # Task summary
        cur.execute("SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status")
        ctx["tasks_by_status"] = {r["status"]: r["cnt"] for r in cur.fetchall()}
        cur.execute("SELECT COUNT(*) as cnt FROM tasks WHERE status NOT IN ('done','cancelled') AND due_date < %s", (hkt_now(),))
        ctx["overdue_tasks"] = dict(cur.fetchone())["cnt"]

        # AI health (latest)
        ctx["ai_health"] = {}
        for ai in ["fighter", "work", "person"]:
            cur.execute("SELECT cpu, mem, disk, uptime, status, recorded_at FROM ai_snapshot WHERE ai_name=%s ORDER BY recorded_at DESC LIMIT 1", (ai,))
            r = cur.fetchone()
            if r:
                row = dict(r)
                row["recorded_at"] = fmt(row["recorded_at"])
                ctx["ai_health"][ai] = row

        # Sync status
        cur.execute("SELECT source, status, message, synced_at FROM sync_status")
        ctx["syncs"] = [{"source": r["source"], "status": r["status"], "message": r["message"],
                         "synced_at": fmt(r["synced_at"])} for r in cur.fetchall()]

        # Recent task activity
        cur.execute("SELECT action, COUNT(*) as cnt FROM task_audit WHERE changed_at >= %s GROUP BY action", (hkt_now() - timedelta(hours=24),))
        ctx["task_activity_24h"] = {r["action"]: r["cnt"] for r in cur.fetchall()}

        # Total insights
        cur.execute("SELECT COUNT(*) as cnt FROM gg_insights")
        ctx["insights_count"] = dict(cur.fetchone())["cnt"]

    # System
    try:
        r = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5)
        ctx["host_uptime"] = r.stdout.strip()
    except: ctx["host_uptime"] = "N/A"

    with open(OUTPUT, "w") as f:
        json.dump(ctx, f, ensure_ascii=False, indent=2)
    print(f"[gg_context] Written to {OUTPUT}")
    return ctx

if __name__ == "__main__":
    collect()
