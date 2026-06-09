---
name: gg-logging-standard
description: >-
  Centralized logging standard for all GG system components (cron jobs, daemons,
  scripts). Every component MUST log start, end, success/failure to the central
  events.jsonl. Use when: (1) creating new scripts/cron jobs, (2) fixing/updating
  existing ones that lack logging, (3) setting up new daemons, (4) auditing system
  health. This is mandatory — no component runs without logging.
---

# GG Logging Standard

## 🎯 Rule

> **Every component MUST log start + end + success/failure to the central log.**
> No exceptions. If a script doesn't log, it's invisible to the error monitor.

## 🗺️ Central Log Files

| Log | Location | Format | Purpose |
|-----|----------|--------|---------|
| Events | `~/.openclaw/logs/gg-v2/events.jsonl` | JSONL | System-wide events (startup, shutdown, errors, heartbeats) |
| Conversation | `~/.openclaw/logs/conversation.jsonl` | JSONL | Messages sent to Terrence/Aggie |
| Cron runs | `~/.openclaw/cron/runs/<job_id>.jsonl` | JSONL (auto) | OpenClaw cron job execution history (auto-generated, no manual log needed) |
| Daemon events | `~/.openclaw/logs/gg-reminder/reminder-events.jsonl` | JSONL | gg_reminder_daemon specific events |

## 📝 Events Log Format (System-wide)

**File**: `~/.openclaw/logs/gg-v2/events.jsonl`

Each line is a JSON object:
```json
{
  "event_id": "SCRIPT-20260522-0001",
  "ts": "2026-05-22T14:00:00+0800",
  "host": "arpa-ai-test01",
  "level": "INFO",
  "category": "run",
  "source": "script_name",
  "message": "Script completed: success"
}
```

### Levels
| Level | When to use |
|-------|------------|
| `INFO` | Normal operation (start, complete) |
| `WARN` | Non-critical issue (API rate limit, invalid input) |
| `ERROR` | Failure (timeout, API error, script crash) |
| `CRITICAL` | System-wide failure (daemon crash, tunnel down) |
| `HEARTBEAT` | Regular health ping (every N cycles) |

### Categories
| Category | When to use |
|----------|------------|
| `run` | Script/cron execution (start + end) |
| `startup` | Daemon/service start |
| `shutdown` | Daemon/service stop |
| `error` | Any failure |
| `deliver` | Message delivery |
| `config` | Config changes |
| `tunnel` | SSH tunnel events |
| `disk` | Disk usage alerts |
| `state` | State file operations |
| `create` | Creating resources |
| `delete` | Deleting resources |

## 🔧 How to Add Logging to Any Script

### Python Scripts
```python
import json, datetime, os, uuid

EVENTS_LOG = os.path.expanduser("~/.openclaw/logs/gg-v2/events.jsonl")
_SCRIPT_NAME = os.path.basename(__file__)
_event_counter = 0

def log_event(level: str, category: str, message: str, **extra):
    global _event_counter
    _event_counter += 1
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    event = {
        "event_id": f"SCRIPT-{now.strftime('%Y%m%d')}-{_event_counter:04d}",
        "ts": now.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "host": "arpa-ai-test01",
        "level": level.upper(),
        "category": category,
        "source": _SCRIPT_NAME,
        "message": message,
        **extra
    }
    os.makedirs(os.path.dirname(EVENTS_LOG), exist_ok=True)
    with open(EVENTS_LOG, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

# Usage:
# log_event("INFO", "run", "Script started")
# try: ... ; log_event("INFO", "run", "Script completed")
# except Exception as e: log_event("ERROR", "error", str(e))
```

### Bash Scripts
```bash
SCRIPT_NAME="$(basename "$0")"

log_event() {
    local level="$1" category="$2" message="$3"
    python3 -c "
import json, datetime, os
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
event = {
    'ts': now.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'host': 'arpa-ai-test01',
    'level': '$level',
    'category': '$category',
    'source': '$SCRIPT_NAME',
    'message': '$message'
}
logfile = os.path.expanduser('~/.openclaw/logs/gg-v2/events.jsonl')
os.makedirs(os.path.dirname(logfile), exist_ok=True)
with open(logfile, 'a') as f:
    f.write(json.dumps(event, ensure_ascii=False) + '\n')
"
}

# Usage:
# log_event INFO run "Script started"
# ... do work ...
# if [ $? -eq 0 ]; then log_event INFO run "Script completed"; else log_event ERROR error "Script failed"; fi
```

## 📋 Standard Log Events Checklist

Every script/daemon must log these minimal events:

| When | Level | Category | Message |
|------|-------|----------|---------|
| Script starts | `INFO` | `run` | "Started" |
| Script completes OK | `INFO` | `run` | "Completed successfully" |
| Script fails | `ERROR` | `error` | Description of what failed |
| Daemon CRITICAL | `CRITICAL` | `error` | "CRITICAL: [details]" |
| Tunnel connects | `INFO` | `tunnel` | "Tunnel UP: port 1890X" |
| Tunnel fails | `ERROR` | `tunnel` | "Tunnel DOWN: port 1890X" |
| Disk >85% | `WARN` | `disk` | "Disk usage: 86%" |

## 🔗 Related Skills
- `system-maintenance.skill.md` — error monitor that reads these logs
- `notion-crm-integration/SKILL.md` — uses `conversation.jsonl` for delivery tracking

## 📋 Script Audit Status (as of 2026-05-22)

| Script | Has Logging? | Priority to Fix |
|--------|-------------|-----------------|
| `scripts/vm/gg_reminder_daemon.py` | ✅ (events.jsonl) | — |
| `scripts/vm/gg_monitor_daemon.py` | ✅ (events.jsonl) | — |
| `scripts/vm/gg_sync_agent.py` | ✅ | — |
| `scripts/vm/nightly_memory_consolidation.py` | ✅ | — |
| `scripts/vm/gg_reminder_monitor.py` | ✅ | — |
| `scripts/vm/gg_repair_spawner.py` | ✅ | — |
| `send_gps_nav_fixed.sh` | ❌ | High |
| `send_traffic_simple.sh` | ❌ | High |
| `send_traffic_to_telegram.sh` | ❌ | High |
| `butler_version_manager.sh` | ❌ | Medium |
| `daily_digest.sh` | ❌ | Medium |
| `smart_butler_evolution.sh` | ⚠️ Partial | Low |
| `daily_memory_extract.sh` | ❌ | Low |
| `commute_google_maps.sh` | ❌ | High |
| `follow_up_manager.sh` | ❌ | Low |
| `gg_morning_briefing_deliver.sh` | ❌ | Low |
| `traffic_scheduler.sh` | ❌ | High |
