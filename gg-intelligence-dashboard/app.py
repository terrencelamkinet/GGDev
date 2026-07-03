#!/usr/bin/env python3
"""3 Servants + Intelligence Dashboard — Flask backend. v2: real SSH health, live tasks, thought bubbles."""
import json, os, sys, subprocess, time, glob, re
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone, timedelta

# PG connection for health check data
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
try:
    from task_hub import pg_cursor
    _HAS_PG = True
except Exception:
    _HAS_PG = False

app = Flask(__name__)
HKT = timezone(timedelta(hours=8))
CORRECT_KEY_PATH = '/tmp/correct_pplx_key.txt'

# ── Helpers ──────────────────────────────────────────────────────────

def hkt_now():
    return datetime.now(HKT)

def read_file_safe(path, default=""):
    try:
        with open(path) as f:
            return f.read().strip()
    except: return default

def read_json_safe(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except: return default if default is not None else {}

# ── Remote Health via SSH ──────────────────────────────────────────

REMOTE_HOSTS = {
    "gg-work": {"host": "gg-work", "label": "Work"},
    "gg-person": {"host": "gg-person", "label": "Person"}
}

def get_remote_health(host_alias):
    """SSH to remote VM and parse real health data."""
    try:
        cmd = f"""ssh {host_alias} '
uptime
echo "---MEM---"
free -m | head -2
echo "---DISK---"
df -h / | tail -1
echo "---PROC---"
ps aux --sort=-%cpu | head -6 | tail -5 | awk "{{print \\$3}}"
'"""
        r = subprocess.run(
            ["ssh", host_alias,
             "uptime; echo '---MEM---'; free -m | head -2; echo '---DISK---'; df -h / | tail -1"],
            capture_output=True, text=True, timeout=8
        )
        if r.returncode != 0:
            return None

        output = r.stdout
        lines = output.strip().split('\n')
        result = {}

        # Parse uptime line: " 16:46:00 up 19 days,  4:20,  1 user,  load average: 1.13, 0.56, 0.42"
        uptime_line = lines[0] if lines else ""
        up_match = re.search(r'up\s+(.+?),\s+\d+\s+user', uptime_line)
        result['uptime'] = up_match.group(1) if up_match else "N/A"

        load_match = re.search(r'load average:\s+([\d.]+)', uptime_line)
        cpu_load = float(load_match.group(1)) if load_match else 0
        result['cpu'] = round(cpu_load * 100 / 2, 1)  # normalize to % (2 cores typical)

        # Parse mem: "Mem:           3915         932         661           0        2612        2983"
        mem_line = None
        for line in lines:
            if line.startswith('Mem:'):
                mem_line = line
                break
        if mem_line:
            parts = mem_line.split()
            if len(parts) >= 3:
                total = float(parts[1])
                used = float(parts[2])
                result['mem_pct'] = round(used / total * 100, 1)
                result['mem_total'] = int(total)
                result['mem_used'] = int(used)

        # Parse disk: "/dev/mapper/ubuntu--vg-ubuntu--lv   19G  9.9G  7.8G  57% /"
        for line in lines:
            if line.startswith('/dev/'):
                disk_parts = line.split()
                if len(disk_parts) >= 5:
                    result['disk_pct'] = disk_parts[4].rstrip('%')

        result['status'] = 'healthy'
        return result
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

def get_local_health():
    """Get real health data from local system."""
    try:
        result = {}
        # Uptime
        r = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5)
        up_match = re.search(r'up\s+(.+?),\s+\d+\s+user', r.stdout)
        result['uptime'] = up_match.group(1) if up_match else "N/A"
        load_match = re.search(r'load average:\s+([\d.]+)', r.stdout)
        cpu_load = float(load_match.group(1)) if load_match else 0
        result['cpu'] = round(cpu_load * 100 / 2, 1)

        # Memory
        r = subprocess.run(["free", "-m"], capture_output=True, text=True, timeout=5)
        for line in r.stdout.split('\n'):
            if line.startswith('Mem:'):
                parts = line.split()
                if len(parts) >= 3:
                    total = float(parts[1])
                    used = float(parts[2])
                    result['mem_pct'] = round(used / total * 100, 1)
                break

        # Disk
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        for line in r.stdout.split('\n'):
            if line.startswith('/dev/'):
                parts = line.split()
                if len(parts) >= 5:
                    result['disk_pct'] = parts[4].rstrip('%')
                break

        result['status'] = 'healthy'
        return result
    except Exception:
        return None

def get_ai_status(name):
    """Get health for local Fighter via system commands, SSH for Work and Person."""
    if name == "Fighter":
        local = get_local_health()
        if local:
            return {
                "name": name,
                "status": local.get("status", "unknown"),
                "cpu": local.get("cpu", "-"),
                "mem": local.get("mem_pct", "-"),
                "disk": local.get("disk_pct", "-"),
                "uptime": local.get("uptime", "N/A"),
                "source": "local"
            }
        return {
            "name": name,
            "status": "unknown",
            "cpu": "-", "mem": "-", "disk": "-",
            "uptime": "N/A", "source": "local"
        }
    else:
        # Remote via SSH
        host_key = "gg-work" if name == "Work" else "gg-person"
        remote = get_remote_health(host_key)
        if remote:
            return {
                "name": name,
                "status": remote.get("status", "unknown"),
                "cpu": remote.get("cpu", "-"),
                "mem": remote.get("mem_pct", "-"),
                "uptime": remote.get("uptime", "N/A"),
                "disk": remote.get("disk_pct", "-"),
                "source": "ssh"
            }
        else:
            return {
                "name": name,
                "status": "unreachable",
                "cpu": "-",
                "mem": "-",
                "uptime": "N/A",
                "disk": "-",
                "source": "ssh"
            }

# ── Dynamic Thought Bubbles ───────────────────────────────────────

def get_latest_thoughts():
    """Extract the latest message per AI from conversation log for thought bubbles."""
    thoughts = {
        "fighter": "Listening...",
        "work": "No recent activity",
        "person": "No recent activity"
    }
    conv_log = "/tmp/ai_conversations.log"
    if not os.path.exists(conv_log):
        return thoughts

    try:
        with open(conv_log) as f:
            lines = f.readlines()

        # Track last message per source
        last_per_source = {}
        for line in reversed(lines):
            try:
                entry = json.loads(line)
                src = entry.get("source", "")
                msg = entry.get("message_preview", "")[:120]
                if not msg:
                    continue
                if src == "hermes-main" and "fighter" not in last_per_source:
                    last_per_source["fighter"] = msg
                elif src == "gg-work" and "work" not in last_per_source:
                    last_per_source["work"] = msg
                elif src == "gg-person" and "person" not in last_per_source:
                    last_per_source["person"] = msg
            except:
                pass

        for key in thoughts:
            if key in last_per_source:
                # Clean up the thought — remove markdown headers, trim
                thought = last_per_source[key]
                thought = re.sub(r'^[#*]{1,3}\s*', '', thought)
                thought = thought.strip()
                if len(thought) > 100:
                    thought = thought[:97] + "..."
                if thought:
                    thoughts[key] = thought
    except:
        pass

    return thoughts

# ── Activity Feed ────────────────────────────────────────────────

def get_activity_feed():
    """Read recent AI conversation + system logs."""
    activities = []
    conv_log = "/tmp/ai_conversations.log"
    if os.path.exists(conv_log):
        with open(conv_log) as f:
            lines = f.readlines()[-30:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                src = entry.get("source", "system")
                tgt = entry.get("target", "")
                msg = entry.get("message_preview", "")[:80]
                ts = entry.get("timestamp", "")
                ai_map = {
                    "hermes-main": {"ai": "fighter", "label": "🔥 Fighter"},
                    "gg-work": {"ai": "work", "label": "⚙️ Work"},
                    "gg-person": {"ai": "person", "label": "❤️ Person"}
                }
                info = ai_map.get(src, {"ai": "system", "label": "System"})
                activities.append({
                    "ai": info["ai"],
                    "label": info["label"],
                    "action": f"→ {tgt}: {msg}" if tgt else msg,
                    "timestamp": ts,
                    "icon": "💬"
                })
            except:
                pass

    # Add cron activity
    cron_file = "/tmp/ai_results/results.jsonl"
    if os.path.exists(cron_file):
        try:
            with open(cron_file) as f:
                lines = f.readlines()[-20:]
                for line in lines:
                    entry = json.loads(line.strip())
                    src = entry.get("source", "")
                    job = entry.get("job", "")
                    summary = entry.get("summary", "")[:80]
                    ts = entry.get("ts", "")
                    ai_map = {
                        "gg-work": ("work", "⚙️ Work"),
                        "gg-person": ("person", "❤️ Person"),
                        "hermes-main": ("fighter", "🔥 Fighter")
                    }
                    info = ai_map.get(src, ("system", "System"))
                    activities.append({
                        "ai": info[0],
                        "label": info[1],
                        "action": f"{job}: {summary}",
                        "timestamp": ts,
                        "icon": "⚡"
                    })
        except: pass

    activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return activities[:20]

def get_mcp_servers():
    """Parse hermes mcp list output for server status."""
    try:
        r = subprocess.run(
            ["hermes", "mcp", "list"],
            capture_output=True, text=True, timeout=10,
            env={**os.environ, "HOME": "/home/airoot"}
        )
        lines = r.stdout.strip().split("\n")
        servers = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("──") or line.startswith("Name"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0].rstrip(":")
                status = "🟢" if "✓" in line else "🔴"
                servers.append({"name": name, "status": status})
        return servers
    except: return []

# ── Real Task Data from Notion Task Center ──────────────────────

def get_notion_tasks():
    """Fetch tasks from Notion Task Center sync state (live data)."""
    sync_file = "/home/airoot/.hermes/task_sync_state.json"
    data = read_json_safe(sync_file, {})
    tasks_dict = data.get("tasks", {})
    if not tasks_dict:
        # Fallback to parsed file if sync unavailable
        fallback = "/tmp/notion_tasks_parsed.json"
        fb_data = read_json_safe(fallback)
        if fb_data:
            fb_tasks = fb_data if isinstance(fb_data, list) else fb_data.get("tasks", [])
            return [t for t in fb_tasks if t.get("status") not in ("Done", "Cancelled", "Archived")][:20]
        return []

    tasks = []
    for page_id, t in tasks_dict.items():
        tasks.append({
            "id": page_id,
            "name": t.get("title", "Untitled"),
            "status": t.get("status", "Not started"),
            "due": t.get("due", ""),
            "area": t.get("area", ""),
            "priority": t.get("priority", ""),
            "done": t.get("status") in ("Done", "Cancelled", "Archived"),
            "notes": (t.get("notes") or "")[:120]
        })

    # Sort: in-progress first, then by due date (closest first), then by status
    def sort_key(t):
        status_order = 0 if t["status"] == "In progress" else 1 if t["status"] == "Not started" else 2
        due = t.get("due") or "9999-12-31"
        return (status_order, due, t["name"])

    tasks.sort(key=sort_key)
    return tasks[:20]

def complete_notion_task(task_id):
    """Mark a task as completed in the Notion sync state file."""
    sync_file = "/home/airoot/.hermes/task_sync_state.json"
    data = read_json_safe(sync_file, {})
    tasks_dict = data.get("tasks", {})
    if task_id in tasks_dict:
        tasks_dict[task_id]["status"] = "Done"
        data["last_sync"] = hkt_now().isoformat()
        data["_updated"] = hkt_now().isoformat()
        with open(sync_file, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    return False

def get_pplx_history():
    history_file = "/tmp/pplx_query_history.json"
    data = read_json_safe(history_file, [])
    return data[-20:]

# ── Perplexity Query Proxy ──────────────────────────────────────────

def call_perplexity(query, mode="ask", recency=None, domains=None, context_size="medium"):
    """Call Perplexity API via REST."""
    model_map = {
        "ask": "sonar-pro",
        "reason": "sonar-reasoning-pro",
        "research": "sonar-deep-research",
        "search": None
    }
    model = model_map.get(mode, "sonar-pro")
    api_key = read_file_safe(CORRECT_KEY_PATH, "")

    if not api_key or len(api_key) < 20:
        return {"ok": False, "error": "API key not configured"}

    import urllib.request, urllib.error

    if mode == "search":
        payload = json.dumps({"query": query}).encode()
        req = urllib.request.Request(
            "https://api.perplexity.ai/search", data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            results = data.get("results", [])
            return {"ok": True, "results": results[:5], "mode": "search"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    else:
        messages = [{"role": "user", "content": query}]
        payload_dict = {"model": model, "messages": messages, "max_tokens": 2000}
        if context_size: payload_dict["search_context_size"] = context_size
        if recency: payload_dict["search_recency_filter"] = recency
        if domains: payload_dict["search_domain_filter"] = domains

        data = json.dumps(payload_dict).encode()
        req = urllib.request.Request(
            "https://api.perplexity.ai/v1/sonar", data=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            citations = result.get("citations", [])
            return {"ok": True, "content": content, "citations": citations[:5], "model": model, "mode": mode}
        except Exception as e:
            return {"ok": False, "error": str(e)}

# ── Routes ──────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/aria/status")
def api_status():
    fighter = get_ai_status("Fighter")
    work = get_ai_status("Work")
    person = get_ai_status("Person")

    # Perplexity status
    api_key = read_file_safe(CORRECT_KEY_PATH, "")
    pplx_status = {
        "layer": "active" if len(api_key) > 20 else "inactive",
        "tools": ["search", "ask", "research", "reason"],
        "queries_today": len(get_pplx_history())
    }

    # Thought bubbles — latest per-AI message
    thoughts = get_latest_thoughts()

    return jsonify({
        "ok": True,
        "fighter": fighter, "work": work, "person": person,
        "perplexity": pplx_status,
        "thoughts": thoughts,
        "timestamp": hkt_now().isoformat()
    })

@app.route("/api/aria/status/history")
def api_status_history():
    """Read AI health history from PG ai_snapshot."""
    if not _HAS_PG:
        return jsonify({"ok": False, "error": "PG not available"})
    try:
        with pg_cursor() as cur:
            cur.execute("""
                SELECT ai_name, status, cpu, mem, disk, uptime, source, recorded_at
                FROM ai_snapshot
                WHERE recorded_at >= %s
                ORDER BY recorded_at DESC
            """, (hkt_now() - timedelta(hours=24),))
            rows = [{
                "ai_name": r["ai_name"], "status": r["status"],
                "cpu": r["cpu"], "mem": r["mem"],
                "disk": r["disk"], "uptime": r["uptime"], "source": r["source"],
                "recorded_at": r["recorded_at"].isoformat()
            } for r in cur.fetchall()]
        return jsonify({"ok": True, "snapshots": rows, "count": len(rows)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/api/aria/activity")
def api_activity():
    activities = get_activity_feed()
    return jsonify({"ok": True, "activities": activities})

@app.route("/api/aria/activity/pg")
def api_activity_pg():
    """Activity feed from PG action_log instead of /tmp/ files."""
    if not _HAS_PG:
        return jsonify({"ok": False, "error": "PG not available"})
    try:
        with pg_cursor() as cur:
            cur.execute("""
                SELECT action_type, entity_ref, detail, created_at
                FROM action_log
                WHERE created_at >= %s
                ORDER BY created_at DESC LIMIT 30
            """, (hkt_now() - timedelta(hours=24),))
            activities = []
            for r in cur.fetchall():
                detail = r.get("detail") or {}
                if isinstance(detail, str):
                    try: detail = json.loads(detail)
                    except: detail = {}
                ai_map = {"fighter": ("fighter", "🔥 Fighter"),
                          "work": ("work", "⚙️ Work"),
                          "person": ("person", "❤️ Person"),
                          "system": ("system", "System")}
                entity = r["entity_ref"] or "system"
                info = ai_map.get(entity, ("system", "System"))
                activities.append({
                    "ai": info[0], "label": info[1],
                    "action": detail.get("message") or detail.get("summary") or r["action_type"],
                    "timestamp": r["created_at"].isoformat() if r["created_at"] else "",
                    "icon": "💬" if r["action_type"] == "conversation" else "⚡"
                })
        return jsonify({"ok": True, "activities": activities, "count": len(activities)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/api/aria/tasks")
def api_tasks():
    tasks = get_notion_tasks()
    now = hkt_now()
    today_str = now.strftime("%Y-%m-%d")
    return jsonify({
        "ok": True,
        "tasks": tasks,
        "total": len(tasks),
        "due_today": [t for t in tasks if t.get("due") == today_str]
    })

@app.route("/api/aria/tasks/pg")
def api_tasks_pg():
    """Tasks from PG tasks table (synced from Notion), with audit history."""
    if not _HAS_PG:
        return jsonify({"ok": False, "error": "PG not available"})
    try:
        with pg_cursor() as cur:
            # Current tasks
            cur.execute("""
                SELECT id, title, status, priority, project, due_date, notes,
                       notion_page_id, created_at, updated_at
                FROM tasks
                WHERE status NOT IN ('done', 'cancelled')
                ORDER BY
                    CASE status WHEN 'in_progress' THEN 0 WHEN 'active' THEN 1 ELSE 2 END,
                    due_date NULLS LAST,
                    created_at DESC
                LIMIT 30
            """)
            tasks = []
            for r in cur.fetchall():
                due = r["due_date"].strftime("%Y-%m-%d") if r.get("due_date") else ""
                tasks.append({
                    "id": str(r["id"]), "notion_id": r["notion_page_id"] or "",
                    "name": r["title"], "title": r["title"],
                    "status": r["status"], "priority": r["priority"],
                    "project": r["project"], "due": due,
                    "notes": (r["notes"] or "")[:120],
                    "done": r["status"] == "done",
                    "created_at": r["created_at"].isoformat() if r["created_at"] else "",
                })

            # Recent audit (last 20 changes)
            cur.execute("""
                SELECT notion_page_id, title, action, old_status, new_status, changed_at
                FROM task_audit
                ORDER BY changed_at DESC LIMIT 20
            """)
            audit = [{
                "page_id": r["notion_page_id"],
                "title": (r["title"] or "")[:40],
                "action": r["action"],
                "old_status": r["old_status"],
                "new_status": r["new_status"],
                "changed_at": r["changed_at"].isoformat() if r["changed_at"] else ""
            } for r in cur.fetchall()]

            # Sync status
            cur.execute("""
                SELECT status, message, rows_synced, synced_at
                FROM sync_status
                WHERE source = 'notion_tasks'
                ORDER BY synced_at DESC LIMIT 1
            """)
            sync = cur.fetchone()
            sync_info = {
                "status": sync["status"] if sync else "unknown",
                "last_sync": sync["synced_at"].isoformat() if sync and sync.get("synced_at") else "",
                "rows": sync["rows_synced"] if sync else 0
            } if sync else {"status": "unknown", "last_sync": "", "rows": 0}

        today_str = hkt_now().strftime("%Y-%m-%d")
        return jsonify({
            "ok": True, "tasks": tasks, "total": len(tasks),
            "due_today": [t for t in tasks if t.get("due") == today_str],
            "audit": audit, "sync": sync_info
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/api/aria/complete-task", methods=["POST"])
def api_complete_task():
    data = request.get_json() or {}
    task_id = data.get("id", "")
    if not task_id:
        return jsonify({"ok": False, "error": "Task ID required"})
    success = complete_notion_task(task_id)
    return jsonify({"ok": success})

@app.route("/api/aria/contracts")
def api_contracts():
    contracts = []
    return jsonify({"ok": True, "contracts": contracts})

@app.route("/api/aria/mcp-status")
def api_mcp_status():
    servers = get_mcp_servers()
    return jsonify({"ok": True, "servers": servers, "total": len(servers)})

@app.route("/api/perplexity/query", methods=["POST"])
def api_pplx_query():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    mode = data.get("mode", "ask")
    recency = data.get("recency")
    domains = data.get("domains")
    context_size = data.get("context_size", "medium")

    if not query:
        return jsonify({"ok": False, "error": "Query required"})

    result = call_perplexity(query, mode, recency, domains, context_size)

    # Save to history
    history_file = "/tmp/pplx_query_history.json"
    history = get_pplx_history()
    history.append({
        "query": query, "mode": mode,
        "timestamp": hkt_now().isoformat(),
        "success": result.get("ok", False)
    })
    try:
        with open(history_file, "w") as f:
            json.dump(history[-50:], f)
    except: pass

    return jsonify(result)

@app.route("/api/perplexity/history")
def api_pplx_history():
    return jsonify({"ok": True, "history": get_pplx_history()})

@app.route("/api/perplexity/history/pg")
def api_pplx_history_pg():
    """Perplexity history from PG pplx_log."""
    if not _HAS_PG:
        return jsonify({"ok": False, "error": "PG not available"})
    try:
        with pg_cursor() as cur:
            cur.execute("""
                SELECT query, mode, success, recorded_at
                FROM pplx_log
                ORDER BY recorded_at DESC LIMIT 20
            """)
            history = [{
                "query": r["query"], "mode": r["mode"],
                "success": r["success"],
                "timestamp": r["recorded_at"].isoformat() if r["recorded_at"] else ""
            } for r in cur.fetchall()]
        return jsonify({"ok": True, "history": history, "count": len(history)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# ── GG Insights ──────────────────────────────────────────────────

@app.route("/api/aria/insights")
def api_insights():
    """Return latest GG insights from gg_insights table."""
    if not _HAS_PG:
        return jsonify({"ok": False, "error": "PG not available"})
    try:
        with pg_cursor() as cur:
            cur.execute("""
                SELECT category, source, title, content, priority, metadata, created_at
                FROM gg_insights
                WHERE created_at >= %s
                ORDER BY
                    CASE priority WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END,
                    created_at DESC
                LIMIT 50
            """, (hkt_now() - timedelta(hours=48),))
            insights = [{
                "category": r["category"], "source": r["source"],
                "title": r["title"], "content": r["content"],
                "priority": r["priority"],
                "meta": r.get("metadata") if isinstance(r.get("metadata"), dict) else
                        (json.loads(r["metadata"]) if r.get("metadata") else {}),
                "created_at": r["created_at"].isoformat() if r["created_at"] else ""
            } for r in cur.fetchall()]

            # Group by category
            grouped = {}
            for ins in insights:
                cat = ins["category"]
                if cat not in grouped: grouped[cat] = []
                grouped[cat].append(ins)

        return jsonify({"ok": True, "insights": insights, "grouped": grouped, "count": len(insights)})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# ── Connection Health ────────────────────────────────────────────────

@app.route("/api/health")
def api_health():
    """Return MCP + API connection status from PG."""
    if not _HAS_PG:
        return jsonify({"ok": False, "error": "PG not available"})
    
    try:
        with pg_cursor() as cur:
            cur.execute("""
                SELECT name, type, category, status, 
                       last_ok, last_fail, last_check, error
                FROM connection_status 
                ORDER BY type DESC, name
            """)
            rows = [dict(r) for r in cur.fetchall()]
            
            cur.execute("""
                SELECT total_connected, total_unknown, total_failed, names_json,
                       snapshot_time
                FROM connection_snapshots 
                ORDER BY snapshot_time DESC LIMIT 1
            """)
            snap = cur.fetchone()
            
            # Get previous snapshot for add/remove
            cur.execute("""
                SELECT names_json FROM connection_snapshots 
                ORDER BY snapshot_time DESC LIMIT 1 OFFSET 1
            """)
            prev = cur.fetchone()
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})
    
    # Calculate adds/removes
    current_names = set(json.loads(snap["names_json"])) if snap else set()
    prev_names = set(json.loads(prev["names_json"])) if prev else set()
    added = list(current_names - prev_names)
    removed = list(prev_names - current_names)
    
    # Format timestamps
    fmt_rows = []
    for r in rows:
        r["last_check_fmt"] = r["last_check"].strftime("%H:%M") if r.get("last_check") else "-"
        
        # Calculate how long in current state (in minutes)
        if r["status"] == "connected":
            dur = 0
        elif r["status"] == "failed" and r.get("last_fail"):
            dur = int((datetime.now(HKT) - r["last_fail"].replace(tzinfo=HKT)).total_seconds() / 60)
        elif r["status"] == "unknown":
            dur = int((datetime.now(HKT) - r["last_check"].replace(tzinfo=HKT)).total_seconds() / 60) if r.get("last_check") else 0
        else:
            dur = 0
        r["duration_min"] = dur
        fmt_rows.append(r)
    
    total = len(fmt_rows)
    conn = sum(1 for r in fmt_rows if r["status"] == "connected")
    unk = sum(1 for r in fmt_rows if r["status"] == "unknown")
    fail = sum(1 for r in fmt_rows if r["status"] == "failed")
    
    return jsonify({
        "ok": True,
        "endpoints": fmt_rows,
        "total": total,
        "connected": conn,
        "unknown": unk,
        "failed": fail,
        "added": added,
        "removed": removed,
        "snapshot_time": snap["snapshot_time"].strftime("%H:%M") if snap else "-",
    })

# ── Main ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7870))
    print(f"🚀 3AI Intelligence Dashboard v2 → http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
