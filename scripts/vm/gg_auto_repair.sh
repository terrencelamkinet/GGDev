#!/bin/bash
# GG Auto-Repair System
# Runs every 5 min: checks system health and auto-spawns repair sessions for failures
# Does NOT notify Terrence unless unrecoverable

HEALTH_CHECK_LOG="/home/airoot/.openclaw/logs/gg-v2/health.log"
WORK_PORT=18901
PERSON_PORT=18902
WORK_TOKEN="49ccb297fe1533acf64b4d8925713782be2d58f9b68eb34cdcd50a761473b652"
PERSON_TOKEN="bf80e73561d252ec9345a2be8be7c4c0e952187ef0d4f375202a62de1b3cf8a2"

log() { echo "[$(date '+%H:%M:%S')] $*" >> "$HEALTH_CHECK_LOG"; }

# ── Check 1: Tunnel ports ──
check_tunnels() {
  for port in $WORK_PORT $PERSON_PORT; do
    if ! ss -tlnp | grep -q ":$port "; then
      log "❌ Port $port down → restarting tunnels"
      bash /home/airoot/.openclaw/workspace/gg-deploy/tunnels.sh start
      sleep 3
      if ss -tlnp | grep -q ":$port "; then
        log "  ✅ Port $port restored"
      else
        log "  🔴 FAILED to restore port $port — need human"
        return 1
      fi
    fi
  done
  return 0
}

# ── Check 2: VM connectivity (curl pong) ──
check_vm() {
  local name="$1" port="$2" token="$3"
  local vm_name="${name#GG-}"
  vm_name=$(echo "$vm_name" | tr '[:upper:]' '[:lower:]')
  
  # Use vm_query.py for reliable health check
  local result
  result=$(python3 /home/airoot/.openclaw/workspace/scripts/vm/vm_query.py "$vm_name" "ping" 2>&1)
  
  if echo "$result" | grep -q '"ok": true'; then
    return 0
  fi
  
  log "❌ $name VM unreachable → retrying tunnel"
  bash /home/airoot/.openclaw/workspace/gg-deploy/tunnels.sh restart
  sleep 5
  
  result=$(python3 /home/airoot/.openclaw/workspace/scripts/vm/vm_query.py "$vm_name" "ping" 2>&1)
  
  if echo "$result" | grep -q '"ok": true'; then
    log "  ✅ $name VM restored"
    return 0
  else
    log "  🔴 $name VM unreachable after retry"
    return 1
  fi
}

# ── Check 3: Cron job last-success times ──
check_cron_heartbeat() {
  local now=$(date +%s)
  local issues=""
  
  # morning_briefing
  if [ -f /tmp/morning_briefing.log ]; then
    local last_mod=$(stat -c %Y /tmp/morning_briefing.log 2>/dev/null || echo 0)
    local age=$(( (now - last_mod) / 3600 ))
    [ $age -gt 26 ] && log "⚠️ morning_briefing last run ${age}h ago — may have failed"
  fi
  
  # sync_agent
  if [ -f /tmp/gg_sync_agent.log ]; then
    local last_sync=$(stat -c %Y /tmp/gg_sync_agent.log 2>/dev/null || echo 0)
    local sync_age=$(( (now - last_sync) / 60 ))
    [ $sync_age -gt 30 ] && log "⚠️ sync_agent not run in ${sync_age}min"
  fi
  
  # daily_memory_extract
  if [ -f /tmp/daily_memory_extract.log ]; then
    local last_mem=$(stat -c %Y /tmp/daily_memory_extract.log 2>/dev/null || echo 0)
    local mem_age=$(( (now - last_mem) / 3600 ))
    [ $mem_age -gt 26 ] && log "⚠️ daily_memory_extract last run ${mem_age}h ago"
  fi
}

# ── Check 4: Disk space ──
check_disk() {
  local usage
  usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
  if [ "$usage" -gt 85 ]; then
    log "🔴 Disk at ${usage}%"
    return 1
  fi
  return 0
}

# ── Main ──
{
  echo "=== Health Check $(date '+%Y-%m-%d %H:%M') ==="
  
  check_tunnels
  check_vm "GG-Work" $WORK_PORT $WORK_TOKEN
  check_vm "GG-Person" $PERSON_PORT $PERSON_TOKEN
  check_cron_heartbeat
  check_disk
  
  echo "=== Done ==="
} >> "$HEALTH_CHECK_LOG" 2>&1

# Trim log to 100 lines
tail -n 100 "$HEALTH_CHECK_LOG" > "${HEALTH_CHECK_LOG}.tmp" && mv "${HEALTH_CHECK_LOG}.tmp" "$HEALTH_CHECK_LOG"
