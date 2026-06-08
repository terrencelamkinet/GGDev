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
        # System data from agents or defaults
        main_agent = data.get("agents", {}).get("main", {}) or {}
        work_agent = data.get("agents", {}).get("work", {}) or {}
        person_agent = data.get("agents", {}).get("person", {}) or {}
        data["system"] = {
            "cpu": main_agent.get("cpu") or work_agent.get("cpu") or 0,
            "mem": main_agent.get("mem") or work_agent.get("mem") or 0,
            "disk": main_agent.get("disk") or work_agent.get("disk") or 0,
            "load": main_agent.get("load") or "0.5",
            "uptime": main_agent.get("uptime") or "N/A",
            "services": {"gg-reminder": "green", "disk": "green", "memory": "green"}
        }
        
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
        
        elif action == "archive":
            # Archive the page (move to trash)
            url = f"https://api.notion.com/v1/pages/{page_id}"
            resp = requests.patch(url, headers=headers, json={"archived": True}, timeout=15)
            if resp.status_code in (200, 201):
                cur, conn = pg_cur()
                if cur:
                    try:
                        cur.execute("UPDATE tasks SET status='cancelled', updated_at=NOW() WHERE notion_page_id=%s", (page_id,))
                        cur.execute("INSERT INTO action_log (action_type, entity_ref, detail) VALUES (%s, %s, %s)",
                                   ("task_archive", "platform", json.dumps({"page_id": page_id})))
                        conn.commit()
                    except Exception as e:
                        print(f"PG archive error: {e}")
                    finally:
                        if conn: conn.close()
                return jsonify({"ok": True, "message": "Task archived"})
            return jsonify({"ok": False, "error": f"Notion API error: {resp.status_code}"}), 502
        
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
                    cur.execute("""INSERT INTO action_log (action_type, entity_ref, detail)
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


# ===== API: CREATE TASK (local PG + optionally Notion) =====

@app.route("/api/task/create", methods=["POST"])
def api_task_create():
    """Create a new task in PG. Notion sync bridge will pick it up."""
    body = request.get_json() or {}
    title = (body.get("title") or "").strip()
    if not title:
        return jsonify({"ok": False, "error": "Title required"}), 400
    
    project = (body.get("project") or "").strip()
    priority = (body.get("priority") or "Q2 · Schedule").strip()
    due = (body.get("due") or "").strip()
    notes = (body.get("notes") or "").strip()
    
    # Map display priority to PG priority
    prio_map = {"Q1 · Do Now": "P0", "Q2 · Schedule": "P2", "Q3 · Delegate": "P3", "Q4 · Eliminate": "P3"}
    pg_priority = prio_map.get(priority, "P2")
    
    # Map display priority to quadrant
    quad_map = {"Q1 · Do Now": "Q1", "Q2 · Schedule": "Q2", "Q3 · Delegate": "Q3", "Q4 · Eliminate": "Q4"}
    quadrant = quad_map.get(priority, "Q2")
    
    cur, conn = pg_cur()
    if not cur:
        return jsonify({"ok": False, "error": "PG unavailable"}), 500
    
    try:
        import uuid as _uuid
        page_id = str(_uuid.uuid4())
        due_val = due if due else None
        
        cur.execute("""
            INSERT INTO tasks (title, priority, quadrant, project, due_date, notes, notion_page_id, status, suggested_delegate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'active', 'self')
            RETURNING id
        """, (title, pg_priority, quadrant, project, due_val, notes, page_id))
        task_id = cur.fetchone()[0]
        
        cur.execute("INSERT INTO action_log (action_type, entity_ref, detail) VALUES (%s, %s, %s)",
                   ("task_create", "platform", json.dumps({"title": title, "project": project})))
        conn.commit()
        
        return jsonify({"ok": True, "id": task_id, "page_id": page_id, "message": f"Task created: {title[:30]}"})
    except Exception as e:
        conn.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        if conn: conn.close()


# ===== API: UPDATE TASK =====

@app.route("/api/task/update", methods=["POST"])
def api_task_update():
    """Update task detail in PG and Notion."""
    body = request.get_json() or {}
    page_id = (body.get("page_id") or "").strip()
    if not page_id:
        return jsonify({"ok": False, "error": "Missing page_id"}), 400
    
    title = (body.get("title") or "").strip()
    notes = (body.get("notes") or "").strip()
    due = (body.get("due") or "").strip()
    priority = (body.get("priority") or "").strip()
    
    # Update PG
    cur, conn = pg_cur()
    if cur:
        try:
            sets = []
            vals = []
            if title:
                sets.append("title=%s"); vals.append(title)
            if notes:
                sets.append("notes=%s"); vals.append(notes)
            if due:
                sets.append("due_date=%s"); vals.append(due)
            if priority:
                prio_map = {"Q1 · Do Now": "P0", "Q2 · Schedule": "P2", "Q3 · Delegate": "P3", "Q4 · Eliminate": "P3"}
                quad_map = {"Q1 · Do Now": "Q1", "Q2 · Schedule": "Q2", "Q3 · Delegate": "Q3", "Q4 · Eliminate": "Q4"}
                pg_p = prio_map.get(priority, "P2")
                pg_q = quad_map.get(priority, "Q2")
                sets.append("priority=%s::priority_level, quadrant=%s::quadrant_type")
                vals.extend([pg_p, pg_q])
            if sets:
                sets.append("updated_at=NOW()")
                vals.append(page_id)
                cur.execute("UPDATE tasks SET " + ", ".join(sets) + " WHERE notion_page_id=%s", vals)
                cur.execute("INSERT INTO action_log (action_type, entity_ref, detail) VALUES (%s, %s, %s)",
                           ("task_update", "platform", json.dumps({"page_id": page_id})))
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"PG update error: {e}")
        finally:
            if conn: conn.close()
    
    # Also update Notion if token available
    if NOTION_TOKEN and (title or due or priority):
        headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
        props = {}
        if title:
            props["Name"] = {"title": [{"text": {"content": title}}]}
        if due:
            props["Due Date"] = {"date": {"start": due}}
        if priority:
            prio_map = {"Q1 · Do Now": "Q1 · Do Now", "Q2 · Schedule": "Q2 · Schedule",
                        "Q3 · Delegate": "Q3 · Delegate", "Q4 · Eliminate": "Q4 · Eliminate"}
            props["Priority"] = {"select": {"name": prio_map.get(priority, "Q2 · Schedule")}}
        if props:
            try:
                requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers,
                              json={"properties": props}, timeout=15)
            except:
                pass
    
    return jsonify({"ok": True, "message": "Task updated"})


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
            cur.execute("""INSERT INTO action_log (action_type, entity_ref, detail)
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


# ===== SERVE TEMPLATES (Webapp Version — NOT DO Static) =====

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

TEMPLATE_MAP = {
    "/": "home.html",
    "/home": "home.html",
    "/intel": "intel.html",
    "/tasks": "tasks.html",
    "/agents": "agents.html",
    "/profile": "profile.html",
    "/system": "profile.html",
}

@app.route("/")
def index():
    return send_from_directory(TEMPLATES_DIR, "home.html")

@app.route("/home")
def home():
    return send_from_directory(TEMPLATES_DIR, "home.html")

@app.route("/intel")
def intel():
    return send_from_directory(TEMPLATES_DIR, "intel.html")

@app.route("/tasks")
def tasks():
    return send_from_directory(TEMPLATES_DIR, "tasks.html")

@app.route("/agents")
def agents():
    return send_from_directory(TEMPLATES_DIR, "agents.html")

@app.route("/profile")
def profile():
    return send_from_directory(TEMPLATES_DIR, "profile.html")

@app.route("/system")
def system():
    return send_from_directory(TEMPLATES_DIR, "profile.html")

@app.route("/agent/<name>")
def agent_detail(name):
    safe_name = name.replace("/", "").replace("\\", "")
    p = os.path.join(TEMPLATES_DIR, "agent_detail.html")
    if os.path.exists(p):
        html = open(p).read()
        return html.replace("{{agent_name}}", safe_name)
    return "Agent detail template not found", 404

# Serve static files (icons, CSS)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

# Catch-all: try templates/, then root/ files, else 404
@app.route("/<path:filename>")
def serve_other(filename):
    # Skip if already handled
    if filename.startswith("static/") or filename.startswith("templates/"):
        return "", 404
    # Try templates first
    tp = os.path.join(TEMPLATES_DIR, filename)
    if os.path.exists(tp) and os.path.isfile(tp):
        return send_from_directory(TEMPLATES_DIR, filename)
    # Then root
    rp = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(rp) and os.path.isfile(rp):
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
