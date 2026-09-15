#!/usr/bin/env python3
"""
GG Repair Spawner — 自動 spawn repair session 俾 GG 主機
當 healing engine 偵測到 CRITICAL 事件無法自動修復時，spawn 一個 repair session

呼叫方式：
  python3 gg_repair_spawner.py

邏輯：
  1. 檢查 events.jsonl 最近5分鐘嘅 CRITICAL 事件
  2. 有新事件就 spawn 一個 repair session
  3. Repair session 會收到 full context（問題描述 + system state）
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

LOG_DIR = os.path.expanduser("~/.openclaw/logs/gg-v2")
EVENTS_FILE = os.path.join(LOG_DIR, "events.jsonl")
SPAWN_MARKER = os.path.join(LOG_DIR, ".last_spawn")
CRITICAL_THRESHOLD_MINUTES = 5  # 5分鐘內冇 spawn 過先 spawn

def get_recent_criticals(within_minutes=5):
    """Fetch CRITICAL events from last N minutes"""
    if not os.path.exists(EVENTS_FILE):
        return []
    
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=within_minutes)
    criticals = []
    
    with open(EVENTS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
                if evt.get("level") == "CRITICAL":
                    # Parse timestamp
                    ts_str = evt.get("ts", "")
                    if ts_str:
                        try:
                            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                            if ts >= cutoff:
                                criticals.append(evt)
                        except:
                            criticals.append(evt)
            except json.JSONDecodeError:
                continue
    
    return criticals

def can_spawn():
    """Check if we can spawn (cooldown)"""
    if not os.path.exists(SPAWN_MARKER):
        return True
    
    try:
        mtime = os.path.getmtime(SPAWN_MARKER)
        age = time.time() - mtime
        return age > CRITICAL_THRESHOLD_MINUTES * 60
    except:
        return True

def mark_spawned():
    """Mark spawn time"""
    with open(SPAWN_MARKER, "w") as f:
        f.write(datetime.now().isoformat())

def build_repair_context(criticals):
    """Build repair context for the spawned session"""
    hostname = os.uname().nodename
    
    lines = [
        f"# 🛠️ GG Auto-Repair Session ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
        f"Host: {hostname}",
        f"",
        f"## Detected CRITICAL Issues (last 5 min)",
    ]
    
    for evt in criticals:
        lines.append(f"- [{evt.get('host','?')}] {evt.get('message','')}")
    
    # Collect system state
    lines.extend([
        f"",
        f"## System State",
    ])
    
    # Disk
    try:
        disk = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        for line in disk.stdout.strip().split("\n"):
            lines.append(f"  {line}")
    except:
        lines.append("  (disk check failed)")
    
    # Memory
    try:
        mem = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5)
        for line in mem.stdout.strip().split("\n"):
            lines.append(f"  {line}")
    except:
        lines.append("  (memory check failed)")
    
    # Processes
    try:
        proc = subprocess.run(["ps", "aux", "--sort=-%cpu", "|", "head", "-8"], capture_output=True, text=True, timeout=5, shell=True)
        lines.append(f"  Top processes:")
        for line in proc.stdout.strip().split("\n")[1:8]:
            if line.strip():
                lines.append(f"  {line}")
    except:
        lines.append("  (process check failed)")
    
    # Health log tail
    health_log = os.path.join(LOG_DIR, "health.log")
    if os.path.exists(health_log):
        try:
            with open(health_log) as f:
                tail = f.readlines()[-20:]
            lines.extend([
                f"",
                f"## Health Log (last 20 lines)",
            ])
            for line in tail:
                lines.append(f"  {line.strip()}")
        except:
            pass
    
    # Tunnels
    lines.extend([
        f"",
        f"## Tunnel Status",
    ])
    try:
        tunnel_result = subprocess.run(
            ["bash", os.path.expanduser("~/.openclaw/workspace/gg-deploy/tunnels.sh"), "status"],
            capture_output=True, text=True, timeout=10
        )
        for line in tunnel_result.stdout.strip().split("\n"):
            if line.strip():
                lines.append(f"  {line}")
    except:
        lines.append("  (tunnel check failed)")
    
    return "\n".join(lines)

def spawn_repair(context):
    """Spawn a repair session using sessions_spawn"""
    task_message = f"""🛠️ GG Auto-Repair triggered by Healing Engine

CRITICAL issues detected on the system. Please investigate and fix:

{context}

DO NOT notify Terrence unless the issue is unrecoverable or requires human intervention.
After fixing, log the repair action and confirm the system is healthy."""

    # Write the repair task to a temp file so the spawning shell can read it
    task_file = "/tmp/gg_repair_task.txt"
    with open(task_file, "w") as f:
        f.write(task_message)
    
    # Log that we're spawning
    print(f"[{datetime.now().isoformat()}] Spawning repair session...")
    print(f"Context: {context[:200]}...")
    
    return task_file

def main():
    criticals = get_recent_criticals()
    
    if not criticals:
        return  # 冇問題，唔 spawn
    
    if not can_spawn():
        print(f"Cooldown active — skipping spawn")
        return
    
    print(f"Found {len(criticals)} CRITICAL event(s)")
    
    context = build_repair_context(criticals)
    task_file = spawn_repair(context)
    
    # Write to log
    evt = {
        "event_id": f"EVT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-SPAWN",
        "ts": datetime.now(timezone.utc).isoformat(),
        "host": os.uname().nodename,
        "level": "INFO",
        "category": "healing",
        "source": "repair_spawner",
        "message": f"Repair session spawned: {len(criticals)} CRITICAL events",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "details": {
            "criticals": [c.get("message", "") for c in criticals],
            "task_file": task_file
        }
    }
    
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(evt) + "\n")
    
    mark_spawned()

if __name__ == "__main__":
    main()
