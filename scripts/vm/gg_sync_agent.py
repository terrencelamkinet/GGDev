#!/usr/bin/env python3
"""
GG Cross-Machine Sync Agent — 每15分鐘 sync 對方做咗咩

用途:
1. 每15分鐘 query GG-Work + GG-Person 嘅 events.jsonl
2. 提取對方最新 events
3. 寫入本地 handoffs.jsonl（顯示對方做咗咩）
4. 確保三部機都知道對方嘅 activity

執行:
  system crontab: */15 * * * * python3 /home/airoot/.openclaw/workspace/scripts/vm/gg_sync_agent.py

原理:
  Main GG → query GG-Work events → write to own handoffs
  Main GG → query GG-Person events → write to own handoffs
  (GG-Work 同 GG-Person 唔直接 sync，因為 tunnels 係單向)
"""
import json, os, sys, subprocess, time
from datetime import datetime, timezone

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG_DIR = os.path.expanduser("~/.openclaw/logs/gg-v2")
SCRIPT_DIR = os.path.join(WORKSPACE, "scripts/vm")

VM_CONFIG = {
    "work": {
        "url": "http://127.0.0.1:18901/v1/chat/completions",
        "token": "49ccb2…b652",
        "name": "GG-Work"
    },
    "person": {
        "url": "http://127.0.0.1:18902/v1/chat/completions",
        "token": "bf80e7…f8a2",
        "name": "GG-Person"
    }
}

def pull_events_from_vm(target):
    """
    Ask a VM to share its recent events.
    Use the VM's memory/log query capability.
    """
    vm = VM_CONFIG[target]
    
    payload = {
        "model": f"openclaw/{vm['name']}",
        "messages": [
            {
                "role": "system",
                "content": "你係 GG 嘅 sync agent。請將你最近嘅 events（來自你嘅 events.jsonl 或者 memory files）"
                           "format 做 JSON array 回傳。每個 event 要有: ts, category, message, level。"
                           "回傳最近5個 events，純 JSON，唔好加解釋。如果冇events就 []"
            },
            {
                "role": "user", 
                "content": "Share your recent activities from the last hour"
            }
        ],
        "max_tokens": 1000
    }
    
    for attempt in range(2):
        try:
            result = subprocess.run([
                "curl", "-s", "--max-time", "60", vm["url"],
                "-H", f"Authorization: Bearer {vm['token']}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(payload)
            ], capture_output=True, text=True, timeout=45)
            
            data = json.loads(result.stdout)
            if "choices" in data and len(data["choices"]) > 0:
                resp_content = data["choices"][0]["message"]["content"].strip()
                # Try to parse as JSON array
                try:
                    events = json.loads(resp_content)
                    if isinstance(events, list):
                        return events
                except json.JSONDecodeError:
                    import re
                    match = re.search(r'\[.*?\]', resp_content, re.DOTALL)
                    if match:
                        try:
                            events = json.loads(match.group())
                            if isinstance(events, list):
                                return events
                        except:
                            pass
                return [{"ts": datetime.now().isoformat(), "category": "sync", 
                         "message": resp_content[:300]}]
            return [{"ts": datetime.now().isoformat(), "category": "error", 
                     "message": f"API error: {data}"}]
        except Exception as e:
            if attempt == 0:
                time.sleep(5)
                continue
            return [{"ts": datetime.now().isoformat(), "category": "error", 
                     "message": f"Failed to sync from {target}: {e}"}]
    
    return []

def write_sync_events(target, events, source_host):
    """Write pulled events to local handoffs.jsonl"""
    handoff_file = os.path.join(LOG_DIR, "handoffs.jsonl")
    ts_now = datetime.now(timezone.utc).isoformat()
    
    for evt in events[-5:]:  # Max 5 per pull
        entry = {
            "ts": evt.get("ts", ts_now),
            "synced_at": ts_now,
            "source_host": source_host,
            "target": target,
            "category": evt.get("category", "unknown"),
            "message": evt.get("message", "")[:300],
            "level": evt.get("level", "INFO")
        }
        
        try:
            os.makedirs(os.path.dirname(handoff_file), exist_ok=True)
            with open(handoff_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

def sync_all():
    """Sync events from all VMs"""
    print(f"🔄 GG Sync Agent — {datetime.now().strftime('%H:%M HKT')}")
    
    for target in ["work", "person"]:
        print(f"  📡 Pulling events from {VM_CONFIG[target]['name']}...")
        events = pull_events_from_vm(target)
        print(f"     Got {len(events)} event(s)")
        
        write_sync_events(target, events, VM_CONFIG[target]['name'])
    
    print("  ✅ Sync complete")

if __name__ == "__main__":
    sync_all()
