#!/usr/bin/env python3
"""
gg_insights_collector.py — Zero-LLM stacking intelligence collector.

RUNS: Every 15 min via cron (no_agent=True, deliver=local)
PURPOSE: Collect real system deltas and append to gg-insights.json
  - NO regenerating existing entries
  - NO LLM calls
  - Only appends genuinely new data

Each entry = {id, ts, source, type, msg, detail?}
  source: fighter | work | person | system
  type: activity | discovery | trend | suggestion | milestone

Preserves existing entries — never rewrites from scratch.
"""

import json, os, subprocess, sys, datetime, socket
from pathlib import Path

HKT = datetime.timezone(datetime.timedelta(hours=8))
NOW = datetime.datetime.now(HKT).strftime("%Y-%m-%d %H:%M")

BASE = Path.home() / "projects/ggdev-repo/gg-dashboard"
DATA_FILE = BASE / "gg-data.json"
INSIGHTS_FILE = BASE / "gg-insights.json"
PUSH_LOG = BASE / "gg-insights-pushed.json"

# === LOAD EXISTING DATA ===

def load_json(path):
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except:
            pass
    return {}

def save_json(path, data):
    # Atomic write to prevent corruption
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(path)

# === COLLECT SYSTEM DELTAS FROM gg-data.json ===

def collect_system_deltas(data, prev_metrics):
    """Compare current gg-data.json with previous metrics snapshot."""
    entries = []
    sys_data = data.get("system", {})

    if not prev_metrics:
        entries.append({
            "id": 0,
            "ts": NOW,
            "source": "system",
            "type": "milestone",
            "msg": "🔧 Intelligence system initialized"
        })
        return entries, {"cpu": sys_data.get("cpu"), "mem": sys_data.get("mem"), "disk": sys_data.get("disk")}

    cpu = sys_data.get("cpu")
    mem = sys_data.get("mem")
    disk = sys_data.get("disk")
    prev_cpu = prev_metrics.get("cpu")
    prev_disk = prev_metrics.get("disk")
    prev_mem = prev_metrics.get("mem")

    if cpu is not None and prev_cpu is not None:
        diff = cpu - prev_cpu
        if abs(diff) >= 20:
            direction = "📈" if diff > 0 else "📉"
            entries.append({
                "id": None, "ts": NOW, "source": "system", "type": "trend",
                "msg": f"{direction} CPU {prev_cpu}% → {cpu}% ({'+' if diff > 0 else ''}{diff}%)"
            })

    if disk is not None and prev_disk is not None:
        diff = disk - prev_disk
        if diff > 3:
            entries.append({
                "id": None, "ts": NOW, "source": "system", "type": "trend",
                "msg": f"💿 Disk usage {prev_disk}% → {disk}% (+{diff}%) — monitoring recommended"
            })

    return entries, {"cpu": cpu, "mem": mem, "disk": disk}

# === COLLECT AGENT ACTIVITY FROM gg-data.json ===

def collect_agent_activity(data, prev_agents):
    """Extract meaningful agent state changes."""
    entries = []
    agents = data.get("agents", {})

    for key, label in [("main", "fighter"), ("work", "work"), ("person", "person")]:
        agent = agents.get(key, {})
        prev = prev_agents.get(key, {})
        thoughts = (agent.get("thoughts") or "").strip()
        prev_thoughts = (prev.get("thoughts") or "").strip()

        # Detect thought changes
        if thoughts and prev_thoughts and thoughts != prev_thoughts:
            entries.append({
                "id": None, "ts": NOW, "source": label, "type": "activity",
                "msg": f"💭 New thought: {thoughts[:80]}{'...' if len(thoughts) > 80 else ''}"
            })

        # Track learnings as discoveries
        learnings = agent.get("learnings") or []
        prev_learnings = prev.get("learnings") or []
        new_learnings = [l for l in learnings if l not in prev_learnings]
        for l in new_learnings:
            entries.append({
                "id": None, "ts": NOW, "source": label, "type": "discovery",
                "msg": f"🔍 Learned: {l[:80]}{'...' if len(l) > 80 else ''}"
            })

        needs = agent.get("needs") or []
        prev_needs = prev.get("needs") or []
        new_needs = [n for n in needs if n not in prev_needs]
        for n in new_needs:
            entries.append({
                "id": None, "ts": NOW, "source": label, "type": "suggestion",
                "msg": f"🎯 New need: {n[:80]}{'...' if len(n) > 80 else ''}"
            })

    return entries, agents

# === COLLECT WORK/PERSON VM ACTIVITY ===

def collect_work_person_vm_activity():
    """SSH to Work/Person VMs for their latest activity (lightweight)."""
    entries = []
    hosts = {
        "work": "172.6.15.181",
        "person": "172.6.15.182"
    }

    for label, host in hosts.items():
        try:
            result = subprocess.run(
                ["ssh", "-oConnectTimeout=5", "-oStrictHostKeyChecking=no",
                 f"airoot@{host}",
                 "cat /tmp/vm_health.log 2>/dev/null | tail -3; "
                 "echo '---'; uptime | awk '{print $3,$4,$5}'; "
                 "echo '---'; ls -lt /tmp/butler*.log /tmp/follow_up*.log /tmp/daily_digest*.log /tmp/traffic_scheduler*.log /tmp/gg_sync*.log 2>/dev/null | head -5"],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout.strip()
            if output:
                lines = [l for l in output.split('\n') if l.strip()]
                for line in lines[:3]:
                    if 'butler' in line.lower() or 'follow_up' in line:
                        entries.append({
                            "id": None, "ts": NOW,
                            "source": label, "type": "activity",
                            "msg": f"📋 Ran: {line.strip()[:60]}"
                        })
                    elif line.startswith('up'):
                        entries.append({
                            "id": None, "ts": NOW,
                            "source": label, "type": "activity",
                            "msg": f"🟢 Uptime: {line.strip()}"
                        })
        except:
            pass
    return entries

# === MAIN COLLECTION CYCLE ===

def main():
    insights = load_json(INSIGHTS_FILE)
    if not insights:
        insights = {"entries": [], "dynamics": {}, "meta": {"total_entries": 0, "last_push_ts": None, "last_collect_ts": None, "version": 1}}
    prev_state = load_json(BASE / ".insights_prev_state.json")
    data = load_json(DATA_FILE)

    new_entries = []
    next_id = max((e.get("id", 0) for e in insights.get("entries", [])), default=0) + 1

    # 1. Collect from system metrics
    sys_entries, new_metrics = collect_system_deltas(data, prev_state.get("metrics", {}))
    for e in sys_entries:
        if e["id"] is None:
            e["id"] = next_id; next_id += 1
        new_entries.append(e)

    # 2. Collect from agent thoughts/learnings/needs changes
    agent_entries, new_agents = collect_agent_activity(data, prev_state.get("agents", {}))
    for e in agent_entries:
        if e["id"] is None:
            e["id"] = next_id; next_id += 1
        new_entries.append(e)

    # [REMOVED] collect_cron_logs() — produced 89% noise entries, no intelligence value
    
    # 3. Collect Work/Person VM activity (lightweight SSH)
    vm_entries = collect_work_person_vm_activity()
    for e in vm_entries:
        if e["id"] is None:
            e["id"] = next_id; next_id += 1
        new_entries.append(e)

    # Append only new entries (don't regenerate)
    if new_entries:
        insights["entries"].extend(new_entries)

        # Update dynamics summary
        agent_data = data.get("agents", {})
        insights["dynamics"] = {
            "fighter": {
                "last_active": NOW,
                "tasks_today": sum(1 for e in insights["entries"] if e.get("source") == "fighter" and e.get("ts", "").startswith(NOW[:10])),
                "discoveries_today": sum(1 for e in insights["entries"] if e.get("source") == "fighter" and e.get("type") == "discovery" and e.get("ts", "").startswith(NOW[:10])),
                "status": "online"
            },
            "work": {
                "last_active": NOW,
                "tasks_today": sum(1 for e in insights["entries"] if e.get("source") == "work" and e.get("ts", "").startswith(NOW[:10])),
                "status": "online",
                "tasks_24h": [e["msg"] for e in reversed(insights["entries"]) if e.get("source") == "work"][:5]
            },
            "person": {
                "last_active": NOW,
                "tasks_today": sum(1 for e in insights["entries"] if e.get("source") == "person" and e.get("ts", "").startswith(NOW[:10])),
                "status": "online",
                "tasks_24h": [e["msg"] for e in reversed(insights["entries"]) if e.get("source") == "person"][:5]
            }
        }

        # Trim to last 200 entries max (don't let file grow forever)
        if len(insights["entries"]) > 200:
            insights["entries"] = insights["entries"][-200:]

    insights["meta"]["total_entries"] = len(insights["entries"])
    insights["meta"]["last_collect_ts"] = NOW
    save_json(INSIGHTS_FILE, insights)

    # Save previous state for delta detection next cycle
    prev_state["metrics"] = new_metrics
    prev_state["agents"] = data.get("agents", {})
    save_json(BASE / ".insights_prev_state.json", prev_state)

    # Output summary for cron logging
    if new_entries:
        print(f"[{NOW}] GG Insights: {len(new_entries)} new entries (total: {len(insights['entries'])})")
        for e in new_entries:
            icon = {"activity": "📋", "discovery": "🔍", "trend": "📊", "suggestion": "🎯", "milestone": "✨"}
            print(f"  {icon.get(e['type'],'📌')} [{e['source']}] {e['msg'][:60]}")
    else:
        print(f"[{NOW}] GG Insights: No changes detected")

if __name__ == "__main__":
    main()
