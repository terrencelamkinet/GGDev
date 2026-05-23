#!/usr/bin/env python3
"""
GG Agent Orchestra v2 — 任務管理同自動記憶委派系統
用法: python3 orchestrate.py <action> [args]

Actions:
  assign work|person <task_desc>  — 分配任務 + 自動記憶委派
  status [id]                      — 查看任務狀態
  list [status|target]             — 列出任務
  complete <id> [result]           — 完成任務
  fail <id> <reason>               — 標記失敗
  memo <work|person> <text>        — 純記憶委派（唔使 task lifecycle）
"""
import json, os, sys, subprocess, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gg_event_logger_v2 import get_logger

TEAM_DIR = os.path.expanduser("~/.openclaw/workspace/team")

VM_CONFIG = {
    "work": {
        "url": "http://127.0.0.1:18901/v1/chat/completions",
        "token": "49ccb297fe1533acf64b4d8925713782be2d58f9b68eb34cdcd50a761473b652",
        "agent": "GG-Work"
    },
    "person": {
        "url": "http://127.0.0.1:18902/v1/chat/completions",
        "token": "bf80e73561d252ec9345a2be8be7c4c0e952187ef0d4f375202a62de1b3cf8a2",
        "agent": "GG-Person"
    }
}

def ts():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M HKT")

def call_vm(target, instruction):
    """Call VM with a task instruction"""
    vm = VM_CONFIG[target]
    payload = {
        "model": f"openclaw/{vm['agent']}",
        "messages": [
            {"role": "system", "content": f"你係 {vm['agent']}，GG 大總管嘅子 agent。收到 task 要執行並回報結果。「回報結果」係指成個任務嘅答案/結果，唔係『已記錄』。用繁體中文（香港用語）。"},
            {"role": "user", "content": instruction}
        ],
        "max_tokens": 1500
    }
    try:
        result = subprocess.run([
            "curl", "-s", vm["url"],
            "-H", f"Authorization: Bearer {vm['token']}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload)
        ], capture_output=True, text=True, timeout=90)
        data = json.loads(result.stdout)
        if "choices" in data and len(data["choices"]) > 0:
            return True, data["choices"][0]["message"]["content"]
        return False, str(data.get("error", "Unknown"))
    except Exception as e:
        return False, str(e)

def assign(target, desc):
    tid = str(uuid.uuid4())[:8]
    task = {
        "id": tid, "target": target, "desc": desc[:200],
        "status": "assigned", "created": ts(), "result": None
    }
    try:
        get_logger().record('command', f'orchestrate assign #{tid}→{target}: {desc[:200]}',
                           source='orchestrate', details={'target': target, 'desc': desc[:100]})
    except Exception:
        pass
    path = f"{TEAM_DIR}/tasks/{tid}_{target}.json"
    ok, result = call_vm(target, desc)
    task["status"] = "done" if ok else "failed"
    task["result"] = result[:500] if result else None
    task["completed"] = ts()
    os.makedirs(f"{TEAM_DIR}/tasks", exist_ok=True)
    with open(path, "w") as f:
        json.dump(task, f, ensure_ascii=False, indent=2)
    return {"ok": ok, "tid": tid, "response": result[:300] if result else None}

def memo(target, text):
    """Pure memory delegation — no task tracking"""
    ok, result = call_vm(target, f"請記錄：{text}")
    # Auto-log with event logger
    try:
        evt_log = get_logger()
        category = 'work_memo' if target == 'work' else 'person_memo'
        evt_log.record('memory', f'orchestrate memo to {target}: {text[:200]}', 
                       source='orchestrate', details={'target': target, 'text': text[:200]})
    except Exception:
        pass
    return {"ok": ok, "response": result[:200] if result else None}

def list_tasks(status=None, target=None):
    tasks = []
    for f in sorted(os.listdir(f"{TEAM_DIR}/tasks")):
        if not f.endswith(".json"): continue
        with open(f"{TEAM_DIR}/tasks/{f}") as fh:
            t = json.load(fh)
            if status and t.get("status") != status: continue
            if target and t.get("target") != target: continue
            tasks.append(t)
    return tasks

def status(tid=None):
    if tid:
        for f in os.listdir(f"{TEAM_DIR}/tasks"):
            if f.startswith(tid) and f.endswith(".json"):
                with open(f"{TEAM_DIR}/tasks/{f}") as fh:
                    return json.load(fh)
        return None
    return list_tasks()

def complete(tid, result_text=None):
    for f in os.listdir(f"{TEAM_DIR}/tasks"):
        if f.startswith(tid) and f.endswith(".json"):
            with open(f"{TEAM_DIR}/tasks/{f}") as fh:
                t = json.load(fh)
            t["status"] = "done"
            t["completed"] = ts()
            if result_text: t["result"] = result_text[:500]
            with open(f"{TEAM_DIR}/tasks/{f}", "w") as fh:
                json.dump(t, fh, ensure_ascii=False, indent=2)
            return t
    return None

def fail(tid, reason):
    for f in os.listdir(f"{TEAM_DIR}/tasks"):
        if f.startswith(tid) and f.endswith(".json"):
            with open(f"{TEAM_DIR}/tasks/{f}") as fh:
                t = json.load(fh)
            t["status"] = "failed"; t["completed"] = ts(); t["result"] = reason[:500]
            with open(f"{TEAM_DIR}/tasks/{f}", "w") as fh:
                json.dump(t, fh, ensure_ascii=False, indent=2)
            return t
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: orchestrate.py <assign|status|list|complete|fail|memo> [args]")
        sys.exit(1)
    a = sys.argv[1]
    if a == "assign" and len(sys.argv) >= 4:
        print(json.dumps(assign(sys.argv[2], " ".join(sys.argv[3:])), ensure_ascii=False, indent=2))
    elif a in ("status", "list"):
        tid = sys.argv[2] if len(sys.argv) > 2 else None
        result = status(tid)
        if isinstance(result, list):
            if not result: print("📭 冇任務")
            for t in result: desc = t.get('desc', t.get('description', t.get('task','?')))[:60]; print(f"  {'✅' if t['status']=='done' else '❌'} #{t['id']}→{t['target']}: {desc} ({t['status']})")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2) if result else "❌ 唔存在")
    elif a == "complete" and len(sys.argv) >= 3:
        r = complete(sys.argv[2], " ".join(sys.argv[3:]) if len(sys.argv)>3 else None)
        print(json.dumps(r, ensure_ascii=False, indent=2) if r else "❌ 唔存在")
    elif a == "fail" and len(sys.argv) >= 4:
        r = fail(sys.argv[2], " ".join(sys.argv[3:]))
        print(json.dumps(r, ensure_ascii=False, indent=2) if r else "❌ 唔存在")
    elif a == "memo" and len(sys.argv) >= 4:
        print(json.dumps(memo(sys.argv[2], " ".join(sys.argv[3:])), ensure_ascii=False, indent=2))
    else:
        print(f"❌ 用法錯誤: {a}")
