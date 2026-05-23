---
name: system-maintenance
description: >-
  System health monitoring, auto-repair, and error escalation. Scope: cron jobs,
  daemon, scripts, config, disk. Auto-fixes known issues silently. Escalates to
  Terrence only when the same error occurs ≥3 times. Use when: (1) cron fails,
  (2) daemon crashes/restarts, (3) script errors, (4) disk usage high, (5) tunnel
  down, (6) heartbeat/timeout events.
---

# System Maintenance Skill

## 🎯 Core Rule

> **Auto-repair silently for known issues. Escalate only when the same error repeats ≥3 times.**

This avoids notification fatigue while still catching systemic problems.

## 📋 Error Registry (centralized)

**Location**: `~/.openclaw/logs/error_registry.json`

Format:
```json
{
  "errors": [
    {
      "id": "cron-ggcheckout-timeout",
      "type": "cron_timeout",
      "source": "da4f8961-c5e6-4479-9456-7c6aeb4c7e74",
      "name": "GG收工打卡",
      "count": 3,
      "first_seen": "2026-05-20T10:00:00Z",
      "last_seen": "2026-05-22T10:00:00Z",
      "auto_fix_applied": false,
      "notified_terrence": false
    }
  ]
}
```

### Error Sources to Track

| Source | Check Method | Auto-fixable? |
|--------|-------------|---------------|
| Cron job runs log | `~/.openclaw/cron/runs/*.jsonl` | ✅ shorten payload or increase timeout |
| Daemon shutdown | `/home/airoot/.openclaw/logs/gg-reminder-daemon.log` | ✅ restart |
| Disk usage | `df -h /` | ⚠️ inform only |
| Tunnel down | `curl localhost:18901/18902` | ✅ auto-reconnect via tunnels.sh |
| Script errors | `~/.openclaw/logs/conversation.jsonl` (source=error) | ⚠️ depends on error |

## 🔧 Auto-Repair Actions (run silently, no notification)

| Error Pattern | Auto-Fix |
|--------------|----------|
| `cron: job execution timed out` | Shorten payload — reduce number of API calls / simplify sub-agent task |
| Daemon CRITICAL exit | Restart via `gg_repair_spawner.py` (already exists) |
| SSH tunnel down | Run `gg-deploy/tunnels.sh reconnect` |
| Stale lock file | Remove `/tmp/gg_reminder_daemon.lock` and restart |

## 🚨 Escalation Rule (notify Terrence)

**Only when `count >= 3`** AND the error is the **exact same type + source + name**.

Escalate via cron (not inline) with summary:
```
⚠️ [source] has failed {N} times since {first_seen}
   Last: {last_seen}
   Auto-fix: {applied/not_applicable}
   Action needed: {suggestion}
```

## 🏗️ Architecture

### Error Monitor Script
Location: `scripts/vm/gg_error_monitor.py`

**Run frequency**: Every 30 minutes (via cron job `0/30 * * * *`)

**Flow**:
```
1. Scan cron runs log for 'error' status entries (last 24h)
2. Scan daemon log for 'CRITICAL' entries (last 24h)
3. Check disk usage >85% → flag
4. Check tunnel ports 18901/18902 → flag
5. Update error_registry.json (group by type+source+name, increment count)
6. For entries with count ≥3 and not yet notified → escalate
7. If entry already notified and still failing → do NOT notify again
```

### Heartbeat Integration
HEARTBEAT.md stays as is — lightweight ping only. Error monitor is separate.

## 🔗 Related System Components

| Component | Location | Role |
|-----------|----------|------|
| Repair spawner | `scripts/vm/gg_repair_spawner.py` | Daemon crash recovery |
| Tunnels script | `gg-deploy/tunnels.sh` | SSH tunnel reconnect |
| Error registry | `~/.openclaw/logs/error_registry.json` | Centralized error state |
| Cron runs log | `~/.openclaw/cron/runs/` | Cron execution history |
