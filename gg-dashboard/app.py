#!/usr/bin/env python3
"""
GG Interactive Platform — Flask backend, PG data, Notion proxy.
Serves interactive dashboard at intel.kinet-poc.com via cloudflared tunnel.
"""
import os, json, sys, uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Load .env for PG credentials
ENV_PATH = os.path.expanduser("~/.hermes/.env")
PG_CONFIG = {
    "host": "127.0.0.1", "port": 5432, "dbname": "task_hub"
}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if line.startswith("PG_USER="):
            PG_CONFIG["user"] = line.split("=", 1)[1]
        elif line.startswith("PG_PASSWORD="):
            PG_CONFIG["password"] = line.split("=", 1)[1]

# Notion config
NOTION_TOKEN = ""
NOTION_DB = "c5d6a00c-b4ab-40e5-ae83-505facd37be0"
# Try multiple locations for Notion key
notion_paths = [
    os.path.expanduser("~/.config/notion/api_key"),
    os.path.expanduser("~/.hermes/.env"),
]
for np in notion_paths:
    if os.path.exists(np):
        with open(np) as f:
            content = f.read().strip()
            if "NOTION_API_KEY=" in content:
                for line in content.split("\n"):
                    if line.startswith("NOTION_API_KEY="):
                        NOTION_TOKEN = line.split("=", 1)[1].strip()
                        break
            elif content.startswith("ntn_"):
                NOTION_TOKEN = content
                break

HKT = timezone(timedelta(hours=8))

try:
    import psycopg2
    HAS_PG = True
except:
    HAS_PG = False

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# ===== PG HELPERS =====

def pg_cur():
    """Return (cursor, connection) or (None, None) on failure."""
    if not HAS_PG:
        return None, None
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        return cur, conn
    except Exception as e:
        print(f"PG connect error: {e}")
        return None, None

# ===== API: ALL DATA (compatible with gg-data.json shape) =====

@app.route("/api/data")
def api_data():
    """Return full dashboard data in gg-data.json compatible format."""
    now = datetime.now(HKT)
    
    data = {
        "ts": now.strftime("%H:%M"),
        "hour": now.hour,
        "minute": now.minute,
        "pushed_at": now.strftime("%Y-%m-%d %H:%M HKT"),
        "badge_color": "green",
        "badge_text": "● Local AI Platform",
        "update_source": "gg_interactive_platform",
        "tasks": {"items": [], "total": 0, "overdue": 0, "due_today": 0, "in_progress": 0, "q1_count": 0, "source": "pg"},
        "activity": [],
        "agents": {},
        "costs": {},
        "schedule": {"today_list": []},
    }
    
    cur, conn = pg_cur()
    if not cur:
        return jsonify(data)
    
    try:
        # Tasks from PG
        cur.execute("""
            SELECT id, title, priority::text, status::text, 
                   quadrant::text, suggested_delegate, project, 
                   due_date::text, notes, notion_page_id,
                   updated_at::text
            FROM tasks 
            WHERE status NOT IN ('done', 'cancelled')
            ORDER BY 
                CASE WHEN due_date < NOW() THEN 0 ELSE 1 END,
                due_date ASC NULLS LAST,
                CASE priority 
                    WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 
                    WHEN 'P2' THEN 2 WHEN 'P3' THEN 3 
                    ELSE 99 END
            LIMIT 50
        """)
        tasks = []
        today_str = now.strftime("%Y-%m-%d")
        overdue = 0; due_today = 0; in_progress = 0; q1 = 0

        # Load area info from Notion sync state file
        area_map = {}
        state_path = os.path.expanduser("~/.hermes/task_sync_state.json")
        if os.path.exists(state_path):
            try:
                with open(state_path) as f:
                    state = json.load(f)
                for pid, tdata in state.get("tasks", {}).items():
                    area_map[pid] = tdata.get("area", "")
            except:
                pass
        
        for r in cur.fetchall():
            tid, title, prio, status, quad, delegate, project, due, notes, nid, updated = r
            area = area_map.get(nid or "", "")
            tasks.append({
                "id": tid, "page_id": nid,
                "title": title or "Untitled",
                "priority": prio or "",
                "status": status or "Not started",
                "quadrant": quad or "",
                "delegate": delegate or "",
                "project": project or "",
                "due": (due or "").split("T")[0] if due else "",
                "notes": notes or "",
                "area": area,
                "last_edited": updated or ""
            })
            if due and due.split("T")[0] < today_str:
                overdue += 1
            if due and due.split("T")[0] == today_str:
                due_today += 1
            if status == "in_progress":
                in_progress += 1
            if prio in ("P0", "P1") or (quad and "Q1" in quad):
                q1 += 1
        
        # Map PG priorities to display format
        prio_map = {"P0": "Q1 · Do Now", "P1": "Q1 · Do Now", "P2": "Q2 · Schedule", "P3": "Q2 · Schedule"}
        for t in tasks:
            p = t["priority"]
            if p in prio_map:
                t["priority"] = prio_map[p]
        
        data["tasks"] = {
            "items": tasks, "total": len(tasks),
            "overdue": overdue, "due_today": due_today,
            "in_progress": in_progress, "q1_count": q1,
            "source": "pg"
        }
        
        # Activity from action_log
        cur.execute("""
            SELECT action_type, entity_ref, detail::text, created_at::text
            FROM action_log ORDER BY created_at DESC LIMIT 30
        """)
        data["activity"] = [
            {"time": (r[3] or "")[11:16] if r[3] else "--:--",
             "text": f"[{r[1] or 'system'}] {r[0]}", "detail": r[2] or ""}
            for r in cur.fetchall()
        ]
        
        # AI health
        cur.execute("""
            SELECT ai_name, status, cpu, mem, disk, uptime, recorded_at::text
            FROM ai_snapshot ORDER BY recorded_at DESC LIMIT 3
        """)
        agents = {}
        for r in cur.fetchall():
            aname, status, cpu, mem, disk, uptime, ts = r
            key = "main" if "main" in (aname or "") or "fighter" in (aname or "") else \
                  "work" if "work" in (aname or "") else "person"
            if key not in agents:
                agents[key] = {"cpu": cpu or 0, "mem": mem or 0, "disk": disk or 0,
                              "uptime": uptime or "", "online": status == "online",
                              "daemons": {"reminder": False, "monitor": False}}
        data["agents"] = agents
        
    except Exception as e:
        print(f"PG read error: {e}")
    finally:
        if conn: conn.close()
    
    return jsonify(data)


# ===== API: TASK ACTION (proxy to Notion) =====

@app.route("/api/task/action", methods=["POST"])
def task_action():
    """Handle task actions: mark_done, set_status, change_due, etc."""
    body = request.get_json() or {}
    action = body.get("action", "")
    page_id = body.get("page_id", "")
    value = body.get("value", "")
    
    if not page_id:
        return jsonify({"ok": False, "error": "Missing page_id"}), 400
    
    if not NOTION_TOKEN:
        return jsonify({"ok": False, "error": "No Notion token configured"}), 500
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        if action == "mark_done":
            props = {"Status": {"status": {"name": "Done"}}, "✅ Done": {"checkbox": True}}
        
        elif action == "set_status":
            valid = ["Not started", "In progress", "Done", "Blocked", "Cancelled"]
            if value not in valid:
                return jsonify({"ok": False, "error": f"Invalid status: {value}"}), 400
            props = {"Status": {"status": {"name": value}}}
        
        elif action == "change_due":
            if not value:
                props = {"Due Date": None}
            else:
                props = {"Due Date": {"date": {"start": value}}}
        
        elif action == "change_priority":
            valid = {"Q1 · Do Now": "Q1 · Do Now", "Q2 · Schedule": "Q2 · Schedule",
                     "Q3 · Delegate": "Q3 · Delegate", "Q4 · Eliminate": "Q4 · Eliminate"}
            if value not in valid:
                return jsonify({"ok": False, "error": f"Invalid priority: {value}"}), 400
            props = {"Priority": {"select": {"name": valid[value]}}}
        
        else:
            return jsonify({"ok": False, "error": f"Unknown action: {action}"}), 400
        
        url = f"https://api.notion.com/v1/pages/{page_id}"
        resp = requests.patch(url, headers=headers, json={"properties": props}, timeout=15)
        
        if resp.status_code in (200, 201):
            # Also update PG
            cur, conn = pg_cur()
            if cur:
                try:
                    if action == "mark_done":
                        cur.execute("UPDATE tasks SET status='done', updated_at=NOW() WHERE notion_page_id=%s", (page_id,))
                    elif action == "set_status":
                        status_map = {"Not started": "active", "In progress": "in_progress", 
                                      "Done": "done", "Blocked": "blocked", "Cancelled": "cancelled"}
                        pg_status = status_map.get(value, "active")
                        cur.execute("UPDATE tasks SET status=%s::task_status, updated_at=NOW() WHERE notion_page_id=%s", 
                                   (pg_status, page_id))
                    
                    # Log action
                    cur.execute("""INSERT INTO action_log (action_type, entity_ref, details)
                        VALUES (%s, %s, %s)""", (f"task_{action}", "platform", 
                        json.dumps({"page_id": page_id, "value": value})))
                    conn.commit()
                except Exception as e:
                    print(f"PG update error: {e}")
                finally:
                    if conn: conn.close()
            
            return jsonify({"ok": True, "message": f"Task {action} successful"})
        
        return jsonify({"ok": False, "error": f"Notion API error: {resp.status_code}"}), 502
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ===== API: AI CHAT (simple prompt relay) =====

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Simple AI chat endpoint. Forwards to action_log for Hermes to pick up."""
    body = request.get_json() or {}
    message = body.get("message", "").strip()
    
    if not message:
        return jsonify({"ok": False, "error": "Empty message"}), 400
    
    cur, conn = pg_cur()
    if cur:
        try:
            cur.execute("""INSERT INTO action_log (action_type, entity_ref, details)
                VALUES ('chat_request', 'platform', %s)""", 
                       (json.dumps({"message": message, "from": "dashboard"}),))
            conn.commit()
        except Exception as e:
            print(f"Chat log PG error: {e}")
        finally:
            if conn: conn.close()
    
    return jsonify({
        "ok": True,
        "message": "✅ Your message has been sent to GG Fighter. I'll get back to you soon!",
        "note": "Message recorded. Fighter will respond in this session."
    })


# ===== API: INSIGHTS =====

@app.route("/api/insights")
def api_insights():
    """Return stacking insights from gg-insights.json."""
    insights_path = os.path.join(os.path.dirname(__file__), "gg-insights.json")
    if os.path.exists(insights_path):
        try:
            with open(insights_path) as f:
                return jsonify(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Insights file read error: {e}")
            return jsonify({"entries": [], "dynamics": {}, "meta": {"total_entries": 0},
                            "error": "Corrupted insights file"}), 500
    return jsonify({"entries": [], "dynamics": {}, "meta": {"total_entries": 0}})


# ===== API: STATUS =====

@app.route("/api/status")
def api_status():
    """Simple health check."""
    return jsonify({
        "status": "ok",
        "mode": "local",
        "pg": HAS_PG,
        "notion": bool(NOTION_TOKEN),
        "timestamp": datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT")
    })


# ===== SERVE TEMPLATES =====

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/legacy")
def legacy():
    return send_from_directory(".", "index.html")

# Serve static files
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "static"), filename)

@app.route("/<path:filename>")
def serve_other(filename):
    # Skip template files — they're broken, use index.html instead
    if filename.startswith("templates/"):
        return "", 404
    path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(path) and os.path.isfile(path):
        return send_from_directory(".", filename)
    return "", 404


# ===== MAIN =====

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7870))
    print(f"🚀 GG Interactive Platform starting on port {port}")
    print(f"   PG: {'connected' if HAS_PG else 'NOT AVAILABLE'}")
    print(f"   Notion: {'configured' if NOTION_TOKEN else 'NOT CONFIGURED'}")
    print(f"   URL: http://localhost:{port}")
    print(f"   Cloudflare: https://intel.kinet-poc.com")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
