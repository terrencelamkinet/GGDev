# Auto-Repair System (2026-05-23 established)

## Decision: Option A — Automatic repair + log (don't notify)

Terrence chose: **Detect → Auto-fix → Log it → Skip notification unless unrecoverable**

## Architecture

### Components

```
gg_healing_engine.sh (cron every 5 min)
  ├── Layer 1: Local health checks (disk/mem/cpu/gateway/network/cron)
  ├── Layer 2: Cross-VM checks (tunnels → auto-fix if broken)
  └── Layer 3: Analyze events → gg_repair_spawner.py
```

### Repair Spawner Flow

```
events.jsonl CRITICAL detected (recent 5min)
  │
  ├── Filter out KNOWN FALSE POSITIVES:
  │   - Kernel cron logs (normal CRON daemon activity)
  │   - Gateway checks during deploy (transient)
  │
  ├── TRUE POSITIVES:
  │   - Tunnel DOWN (Work or Person) → run tunnels.sh restart
  │   - Disk > 90% → journalctl vacuum + apt clean
  │   - Gateway DOWN → systemctl restart openclaw
  │   - Memory > 90% → report only (no auto-fix action)
  │
  └── After auto-fix:
      ├── Verify fix succeeded
      ├── Log to events.jsonl (INFO level)
      └── DO NOT notify Terrence unless unrecoverable
```

### Known False Positives to Filter

| Pattern | Why it's triggered | Action |
|---------|-------------------|--------|
| `Kernel: ... CRON...CMD (python3 ...)` | `/var/log/syslog` entries for every cron run | **Filter out** — normal |
| `gg-monitor: Cron stale: ...` | Some crons stopped running (by design) | **Filter out** if < 48h stale |
| Gateway check during deploy | Gateway restart during deploy = transient | Retry 2x before flagging |

### Repair Actions (auto-execute)

| Issue | Auto-action | Verify |
|-------|-----------|--------|
| Tunnel down (SSH OK) | `tunnels.sh restart` | `curl localhost:PORT/health` |
| Both tunnels down | `tunnels.sh restart`, wait 6s, check | Same |
| Disk > 90% | `journalctl --vacuum-time=3d`, `apt-get clean` | `df /` |
| Gateway fail | `systemctl --user restart openclaw`, wait 8s | Retry API call |
| Sub-agent session stuck | `gg_subagent_watchdog.py` handles this | Watchdog logs |

### Notification Rules

- ✅ Auto-fix succeeded (from known fix list) → **Log only, no notification**
- ⚠️ Auto-fix failed → Log + **flag in events.jsonl** (waits for Terrence to ask)
- 🔴 Unrecoverable (e.g., VM unreachable via SSH/tunnel) → **Spawning repair session** with context
- 🔴 New error pattern (not in known fix list) → **Spawning repair session**

### Metrics

Success rate of auto-fix actions:
- Tunnel restart: verified today (manual). Auto-fix pending validation.
- Disk cleanup: in healing engine already (works).
- Gateway restart: in healing engine already.

### Implementation Changes

1. **gg_repair_spawner.py** — Add:
   - `filter_false_positives()` — removes known noise
   - `auto_fix()` — executes fix actions directly (not just spawn)
   - For each known fix, try auto-fix first; only spawn session if fix fails
   - Cooldown: 5 min per issue type (not global — tunnel cooldown separate from disk cooldown)

2. **gg_healing_engine.sh** — Already has auto-fix for:
   - Disk (journalctl cleanup when >90%)
   - Gateway (restart on fail)
   - Tunnels (restart when both down)
   - Just need to fix false positive filtering for cron events

3. Current issues to fix:
   - Healing engine marks cron execution as CRITICAL (false positive)
   - Cooldown too aggressive (global 5min, stops tunnel repair while disk still warm)
