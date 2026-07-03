#!/usr/bin/env python3
"""
sync_to_pg.py — Unified 15-min sync: Notion tasks + AI health + activity + perplexity → PG.
Notion is source of truth for tasks. PG augments with audit trail & metadata.
"""
import os, sys, json, subprocess, re, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta, date
from pathlib import Path

HOME = Path.home()
HKT = timezone(timedelta(hours=8))

sys.path.insert(0, str(HOME / ".hermes" / "scripts"))
from task_hub import pg_cursor

# ── Paths ──
TASK_SYNC_FILE = HOME / ".hermes" / "task_sync_state.json"
CONV_LOG = "/tmp/ai_conversations.log"
RESULTS_LOG = "/tmp/ai_results/results.jsonl"
PPLX_HISTORY_FILE = "/tmp/pplx_query_history.json"
CORRECT_KEY_PATH = "/tmp/correct_pplx_key.txt"

REMOTE_HOSTS = {"gg-work": "Work", "gg-person": "Person"}

# ── Helpers ──
def hkt_now():
    return datetime.now(HKT)

def read_json_safe(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except: return default if default is not None else {}

def read_file_safe(path, default=""):
    try: return Path(path).read_text().strip()
    except: return default

# ═══ 1. TASK SYNC (Notion → PG + audit trail) ═══

def list_pg_tasks():
    """Get current PG task set by notion_page_id."""
    with pg_cursor() as cur:
        cur.execute("SELECT notion_page_id, status, updated_at FROM tasks WHERE notion_page_id IS NOT NULL")
        return {r["notion_page_id"]: {"status": r["status"], "updated_at": r["updated_at"]}
                for r in cur.fetchall()}

def ensure_task_audit_table():
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS task_audit (
                id BIGSERIAL PRIMARY KEY,
                notion_page_id TEXT NOT NULL,
                title TEXT,
                action TEXT NOT NULL,
                old_status TEXT,
                new_status TEXT,
                changed_at TIMESTAMPTZ,
                synced_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_audit_page ON task_audit(notion_page_id)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_audit_time ON task_audit(changed_at DESC)
        """)

def map_notion_status(s):
    """Map Notion status string to task_status enum."""
    m = {"Done": "done", "In progress": "in_progress", "Not started": "active",
         "Cancelled": "cancelled", "Archived": "cancelled"}
    return m.get(s, "active")

def map_notion_priority(s):
    s = (s or "").upper().strip()
    if s in ("P0", "P1", "P2", "P3"): return s
    if "URGENT" in s or s == "P0": return "P0"
    if s in ("HIGH", "H"): return "P1"
    if s in ("MEDIUM", "M"): return "P2"
    return "P3"

def sync_tasks():
    """Sync Notion tasks → PG. Write audit on changes."""
    now = hkt_now()
    state = read_json_safe(TASK_SYNC_FILE, {"tasks": {}, "last_sync": None})
    notion_tasks = state.get("tasks", {})
    if not notion_tasks:
        print("[sync_tasks] No tasks in state file — skip")
        return 0

    pg_tasks = list_pg_tasks()
    changes = 0

    with pg_cursor(commit=True) as cur:
        for page_id, t in notion_tasks.items():
            title = t.get("title", "Untitled")
            status = map_notion_status(t.get("status", "Not started"))
            priority = map_notion_priority(t.get("priority", ""))
            area = t.get("area", "")
            due = t.get("due", "")
            project = t.get("project", "")
            notes = t.get("notes", "")

            old = pg_tasks.get(page_id)
            old_status = old["status"] if old else None

            # Upsert into tasks table (by notion_page_id)
            cur.execute("""
                UPDATE tasks SET title=%s, status=%s, priority=%s, project=%s,
                    due_date=%s, notes=%s, updated_at=%s
                WHERE notion_page_id=%s
            """, (title, status, priority, project, due if due else None,
                  notes, now, page_id))
            if cur.rowcount == 0:
                # New task from Notion
                cur.execute("""
                    INSERT INTO tasks (id, title, status, priority, project, due_date, notes,
                        created_by, created_at, updated_at, notion_page_id)
                    VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s,
                        'notion', %s, %s, %s)
                """, (title, status, priority, project, due if due else None,
                      notes, now, now, page_id))
                # Audit: created
                cur.execute("""
                    INSERT INTO task_audit (notion_page_id, title, action, old_status, new_status, changed_at)
                    VALUES (%s, %s, 'created', NULL, %s, %s)
                """, (page_id, title, status, now))
                changes += 1
            elif old and old_status != status:
                # Map Notion status → enum for audit
                old_enum = map_notion_status(old_status)
                new_enum = status
                action_map = {
                    ("in_progress", "done"): "completed",
                    ("done", "in_progress"): "resumed",
                    ("active", "done"): "completed",
                }
                action = action_map.get((old_enum, new_enum), "status_changed")
                cur.execute("""
                    INSERT INTO task_audit (notion_page_id, title, action, old_status, new_status, changed_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (page_id, title, action, old_enum, new_enum, now))
                changes += 1

        # Detect tasks removed from Notion (archived/untrashed?)
        pg_page_ids = set(pg_tasks.keys())
        notion_page_ids = set(notion_tasks.keys())
        removed = pg_page_ids - notion_page_ids
        for page_id in removed:
            # Don't delete — mark as not visible
            if pg_tasks[page_id]["status"] not in ("Done", "Cancelled", "Archived"):
                cur.execute("""
                    INSERT INTO task_audit (notion_page_id, title, action, old_status, new_status, changed_at)
                    VALUES (%s, 'Unknown', 'removed_from_notion', %s, 'Archived', %s)
                """, (page_id, pg_tasks[page_id]["status"], now))
                changes += 1

    print(f"[sync_tasks] {len(notion_tasks)} Notion tasks, {changes} changes")
    return changes

# ═══ 2. AI HEALTH SNAPSHOT ═══

def ensure_ai_snapshot_table():
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ai_snapshot (
                id BIGSERIAL PRIMARY KEY,
                ai_name TEXT NOT NULL,
                status TEXT,
                cpu REAL,
                mem REAL,
                disk TEXT,
                uptime TEXT,
                source TEXT,
                recorded_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_ai_snapshot_time ON ai_snapshot(recorded_at DESC)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_ai_snapshot_name ON ai_snapshot(ai_name)
        """)

def get_local_health():
    try:
        r = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5)
        up_match = re.search(r'up\s+(.+?),', r.stdout)
        load_match = re.search(r'load average:\s+([\d.]+)', r.stdout)
        cpu = round(float(load_match.group(1)) * 100 / 2, 1) if load_match else 0
        r2 = subprocess.run(["free", "-m"], capture_output=True, text=True, timeout=5)
        mem_pct = 0
        for line in r2.stdout.split('\n'):
            if line.startswith('Mem:'):
                parts = line.split()
                if len(parts) >= 3: mem_pct = round(float(parts[2]) / float(parts[1]) * 100, 1)
        r3 = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        disk = ""
        for line in r3.stdout.split('\n'):
            if line.startswith('/dev/'):
                disk = line.split()[4].rstrip('%') if len(line.split()) >= 5 else ""
        return {"status": "healthy", "cpu": cpu, "mem": mem_pct,
                "disk": disk, "uptime": up_match.group(1) if up_match else "N/A"}
    except: return None

def get_remote_health(host_alias):
    try:
        r = subprocess.run(["ssh", host_alias,
            "uptime; echo '---'; free -m | head -2; echo '---'; df -h / | tail -1"],
            capture_output=True, text=True, timeout=8)
        if r.returncode != 0: return None
        lines = r.stdout.strip().split('\n')
        result = {}
        up_match = re.search(r'up\s+(.+?),', lines[0])
        result['uptime'] = up_match.group(1) if up_match else "N/A"
        load_match = re.search(r'load average:\s+([\d.]+)', lines[0])
        result['cpu'] = round(float(load_match.group(1)) * 100 / 2, 1) if load_match else 0
        for line in lines:
            if line.startswith('Mem:'):
                parts = line.split()
                if len(parts) >= 3: result['mem'] = round(float(parts[2]) / float(parts[1]) * 100, 1)
            if line.startswith('/dev/'):
                dp = line.split()
                if len(dp) >= 5: result['disk'] = dp[4].rstrip('%')
        result['status'] = 'healthy'
        return result
    except: return None

def sync_ai_health():
    """Take health snapshot of all 3 AIs, write to PG."""
    now = hkt_now()

    # Fighter (local)
    local = get_local_health()
    fighter = local if local else {"status": "unknown", "cpu": 0, "mem": 0, "disk": "", "uptime": "N/A"}

    # Work & Person (SSH)
    work = get_remote_health("gg-work")
    person = get_remote_health("gg-person")

    entries = [
        ("fighter", fighter, "local"),
        ("work", work if work else {"status": "unreachable", "cpu": 0, "mem": 0, "disk": "", "uptime": "N/A"}, "ssh"),
        ("person", person if person else {"status": "unreachable", "cpu": 0, "mem": 0, "disk": "", "uptime": "N/A"}, "ssh"),
    ]

    with pg_cursor(commit=True) as cur:
        for name, data, src in entries:
            cur.execute("""
                INSERT INTO ai_snapshot (ai_name, status, cpu, mem, disk, uptime, source, recorded_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, data.get("status"), data.get("cpu"), data.get("mem"),
                  str(data.get("disk", "")), data.get("uptime", "N/A"), src, now))

    print(f"[sync_ai_health] fighter={'ok' if local else 'fail'} "
          f"work={'ok' if work else 'fail'} person={'ok' if person else 'fail'}")
    return 1

# ═══ 3. ACTIVITY LOG ═══

def ensure_activity_log_table():
    """action_log already exists — just check it has the right structure."""
    pass  # action_log already has: action_type, entity_ref, detail (jsonb), created_at

def sync_activity():
    """Read conversation + cron logs, write to action_log."""
    now = hkt_now()
    count = 0

    with pg_cursor(commit=True) as cur:
        # 1. Conversation log
        if os.path.exists(CONV_LOG):
            try:
                with open(CONV_LOG) as f:
                    for line in f.readlines()[-50:]:
                        try:
                            entry = json.loads(line.strip())
                            src = entry.get("source", "system")
                            tgt = entry.get("target", "")
                            msg = (entry.get("message_preview", "") or "")[:120]
                            ts = entry.get("timestamp", "")
                            ai_map = {"hermes-main": "fighter", "gg-work": "work", "gg-person": "person"}
                            ai_name = ai_map.get(src, "system")
                            cur.execute("""
                                INSERT INTO action_log (action_type, entity_ref, detail, created_at)
                                VALUES (%s, %s, %s, %s)
                            """, ("conversation", ai_name, json.dumps({
                                "source": src, "target": tgt, "message": msg
                            }), now))
                            count += 1
                        except: pass
            except: pass

        # 2. Cron results
        if os.path.exists(RESULTS_LOG):
            try:
                with open(RESULTS_LOG) as f:
                    for line in f.readlines()[-30:]:
                        try:
                            entry = json.loads(line.strip())
                            cur.execute("""
                                INSERT INTO action_log (action_type, entity_ref, detail, created_at)
                                VALUES (%s, %s, %s, %s)
                            """, ("cron", entry.get("job", "?"), json.dumps({
                                "source": entry.get("source", ""),
                                "summary": (entry.get("summary", "") or "")[:80]
                            }), now))
                            count += 1
                        except: pass
            except: pass

    print(f"[sync_activity] {count} entries")
    return count

# ═══ 4. PERPLEXITY LOG ═══

def ensure_pplx_log_table():
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pplx_log (
                id BIGSERIAL PRIMARY KEY,
                query TEXT,
                mode TEXT,
                success BOOLEAN,
                response_preview TEXT,
                recorded_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_pplx_log_time ON pplx_log(recorded_at DESC)")

def sync_pplx():
    data = read_json_safe(PPLX_HISTORY_FILE, [])
    if not data:
        print("[sync_pplx] No history — skip")
        return 0
    count = 0
    with pg_cursor(commit=True) as cur:
        for entry in data[-30:]:
            query = (entry.get("query", "") or "")[:200]
            mode = entry.get("mode", "ask")
            success = entry.get("success", False)
            ts = entry.get("timestamp", "")
            try:
                parsed_ts = datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else now
            except: parsed_ts = hkt_now()
            cur.execute("""
                INSERT INTO pplx_log (query, mode, success, response_preview, recorded_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (query, mode, success, query[:60], parsed_ts))
            count += 1
    print(f"[sync_pplx] {count} entries")
    return count

# ═══ 5. SYNC STATUS ═══

def ensure_sync_status_table():
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sync_status (
                source TEXT PRIMARY KEY,
                status TEXT,
                message TEXT,
                rows_synced INTEGER DEFAULT 0,
                synced_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)

def update_sync_status(source, status, message="", rows=0):
    with pg_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO sync_status (source, status, message, rows_synced, synced_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source) DO UPDATE SET
                status=%s, message=%s, rows_synced=%s, synced_at=%s
        """, (source, status, message, rows, hkt_now(), status, message, rows, hkt_now()))

# ═══ MAIN ═══

def main():
    print(f"=== sync_to_pg @ {hkt_now().strftime('%H:%M')} ===")

    # Ensure tables
    ensure_task_audit_table()
    ensure_ai_snapshot_table()
    ensure_pplx_log_table()
    ensure_sync_status_table()

    # Sync each source
    try:
        n = sync_tasks()
        update_sync_status("notion_tasks", "ok", f"{n} changes", n)
    except Exception as e:
        update_sync_status("notion_tasks", "error", str(e)[:100])
        print(f"[ERROR] tasks: {e}")

    try:
        a = sync_ai_health()
        update_sync_status("ai_health", "ok", "snapshot taken", a)
    except Exception as e:
        update_sync_status("ai_health", "error", str(e)[:100])
        print(f"[ERROR] ai: {e}")

    try:
        c = sync_activity()
        update_sync_status("activity_log", "ok", f"{c} entries", c)
    except Exception as e:
        update_sync_status("activity_log", "error", str(e)[:100])
        print(f"[ERROR] activity: {e}")

    try:
        p = sync_pplx()
        update_sync_status("pplx_log", "ok", f"{p} entries", p)
    except Exception as e:
        update_sync_status("pplx_log", "error", str(e)[:100])
        print(f"[ERROR] pplx: {e}")

    # GG Insights data facts (every 15min)
    try:
        insights_script = str(HOME / "projects/gg-intelligence-dashboard/gg_insights_v2.py")
        r = subprocess.run(["python3", insights_script], capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            update_sync_status("gg_insights", "ok", "insights generated")
        else:
            update_sync_status("gg_insights", "error", (r.stderr or "")[:80])
    except Exception as e:
        update_sync_status("gg_insights", "error", str(e)[:80])

    print("=== sync complete ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
