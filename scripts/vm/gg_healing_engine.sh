#!/bin/bash
# ═══════════════════════════════════════════════════════════
# GG Healing Engine v2 — 三機完整自我修復系統
# 每5分鐘 cron 觸發，三部機各自執行
# ═══════════════════════════════════════════════════════════

set -o pipefail

HEALTH_LOG="/home/airoot/.openclaw/logs/gg-v2/health.log"
EVENTS_LOG="/home/airoot/.openclaw/logs/gg-v2/events.jsonl"
MY_HOST=$(hostname)
MY_IS_MAIN=false

[ "$MY_HOST" = "arpa-ai-test01" ] && MY_IS_MAIN=true
[ "$MY_HOST" = "gg-main" ] && MY_IS_MAIN=true

# Gateway token from local config
GW_TOKEN=$(sudo -u airoot python3 -c "
import json
try:
    g = json.load(open('/home/airoot/.openclaw/openclaw.json'))
    print(g['gateway']['auth']['token'])
except:
    print('')
" 2>/dev/null)

WORK_HOST="172.6.15.181"
PERSON_HOST="172.6.15.182"
SSH_KEY="/home/airoot/.ssh/gg_subagent"

log() { echo "[$(date '+%H:%M:%S')] $*" >> "$HEALTH_LOG"; }

report_critical() {
  log "🔴 CRITICAL: $1"
  echo "{\"event_id\":\"EVT-$(date +%Y%m%d-%H%M%S)\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"host\":\"$MY_HOST\",\"level\":\"CRITICAL\",\"category\":\"healing\",\"source\":\"healing_engine\",\"message\":\"$1\",\"date\":\"$(date +%Y-%m-%d)\"}" >> "$EVENTS_LOG"
}

report_warn() {
  log "⚠️ WARN: $1"
  echo "{\"event_id\":\"EVT-$(date +%Y%m%d-%H%M%S)-W\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"host\":\"$MY_HOST\",\"level\":\"WARN\",\"category\":\"healing\",\"source\":\"healing_engine\",\"message\":\"$1\",\"date\":\"$(date +%Y-%m-%d)\"}" >> "$EVENTS_LOG"
}

report_info() {
  echo "{\"event_id\":\"EVT-$(date +%Y%m%d-%H%M%S)-I\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"host\":\"$MY_HOST\",\"level\":\"INFO\",\"category\":\"healing\",\"source\":\"healing_engine\",\"message\":\"$1\",\"date\":\"$(date +%Y-%m-%d)\"}" >> "$EVENTS_LOG"
}

# ─────────────────────────────────────────────────────────
# Layer 1: 本機檢測（三部機獨立執行）
# ─────────────────────────────────────────────────────────

check_gateway() {
  local result
  result=$(curl -s --max-time 10 "http://127.0.0.1:18789/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GW_TOKEN" \
    -d '{"messages":[{"role":"user","content":"ping"}]}' 2>&1)

  if echo "$result" | grep -q '"finish_reason":"stop"'; then
    log "✅ Gateway OK"
    return 0
  fi

  report_warn "Gateway FAIL — restarting"
  systemctl --user restart openclaw 2>/dev/null || true
  sleep 8
  local retry
  retry=$(curl -s --max-time 10 "http://127.0.0.1:18789/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GW_TOKEN" \
    -d '{"messages":[{"role":"user","content":"ping"}]}' 2>&1)
  if echo "$retry" | grep -q "finish_reason"; then
    log "  ✅ Gateway restored"; report_info "Gateway restored after restart"
  else
    report_critical "Gateway STILL DOWN after restart"
  fi
}

check_disk() {
  local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
  if [ "$usage" -gt 90 ]; then
    report_critical "Disk ${usage}%"
    sudo journalctl --vacuum-time=3d 2>/dev/null || true
    sudo apt-get clean 2>/dev/null || true
  elif [ "$usage" -gt 80 ]; then
    report_warn "Disk ${usage}%"
  else
    log "✅ Disk ${usage}%"
  fi
}

check_memory() {
  local total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  local free=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
  local pct=$(( (total - free) * 100 / total ))
  [ "$pct" -gt 90 ] && report_warn "Memory ${pct}%" || log "✅ Memory ${pct}%"
}

check_cpu() {
  local load=$(cut -d' ' -f1 /proc/loadavg)
  local cores=$(nproc)
  local pct=$(echo "$load $cores" | awk '{printf "%d", ($1/$2)*100}')
  [ "$pct" -gt 90 ] && report_warn "CPU ${pct}%" || log "✅ CPU ${pct}%"
}

check_network() {
  local dns=$(dig +short google.com @8.8.8.8 2>&1 | head -1)
  [ -z "$dns" ] && report_warn "DNS failed" || log "✅ Network OK"
}

check_crons() {
  local now=$(date +%s)
  for f in /tmp/daily_memory_extract.log /tmp/nightly_memory_consolidation.log; do
    if [ -f "$f" ]; then
      local age=$(( (now - $(stat -c %Y "$f" 2>/dev/null || echo 0)) / 3600 ))
      [ "$age" -gt 28 ] && report_warn "$(basename $f) stale (${age}h)"
    fi
  done
}

# ─────────────────────────────────────────────────────────
# Layer 2: 主機專有跨機檢測（只有 Main GG 執行）
# ─────────────────────────────────────────────────────────

check_vm_tier() {
  # 先 tunnel 測試，如果失敗先 SSH
  local w_ok=false p_ok=false
  
  local w_result=$(python3 /home/airoot/.openclaw/workspace/scripts/vm/vm_query.py "work" "ping" 2>&1)
  echo "$w_result" | grep -q '"ok": true' && w_ok=true
  
  local p_result=$(python3 /home/airoot/.openclaw/workspace/scripts/vm/vm_query.py "person" "ping" 2>&1)
  echo "$p_result" | grep -q '"ok": true' && p_ok=true
  
  $w_ok && log "✅ GG-Work via tunnel" || log "❌ GG-Work tunnel fail"
  $p_ok && log "✅ GG-Person via tunnel" || log "❌ GG-Person tunnel fail"
  
  # 如果兩邊都 fail，一次過 rebuild tunnels
  if ! $w_ok && ! $p_ok; then
    log "  🔄 Rebuilding tunnels (both down)"
    bash /home/airoot/.openclaw/workspace/gg-deploy/tunnels.sh restart
    sleep 6
    w_result=$(python3 /home/airoot/.openclaw/workspace/scripts/vm/vm_query.py "work" "ping" 2>&1)
    p_result=$(python3 /home/airoot/.openclaw/workspace/scripts/vm/vm_query.py "person" "ping" 2>&1)
    echo "$w_result" | grep -q '"ok": true' && log "  ✅ Work restored" || report_critical "Work still down after rebuild"
    echo "$p_result" | grep -q '"ok": true' && log "  ✅ Person restored" || report_critical "Person still down after rebuild"
  fi

  # 如果只有一邊 fail，直接 SSH bypass 確認
  if ! $w_ok && $p_ok; then
    local s=$(ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=10 airoot@$WORK_HOST "echo ok" 2>&1)
    [ "$s" = "ok" ] && report_warn "Work tunnel broken (SSH OK)" || report_critical "Work SSH FAIL — may be OFFLINE"
  fi
  if $w_ok && ! $p_ok; then
    local s=$(ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=10 airoot@$PERSON_HOST "echo ok" 2>&1)
    [ "$s" = "ok" ] && report_warn "Person tunnel broken (SSH OK)" || report_critical "Person SSH FAIL — may be OFFLINE"
  fi
}

check_sync_agent() {
  [ ! -f /tmp/gg_sync_agent.log ] && return
  local last=$(tail -1 /tmp/gg_sync_agent.log 2>/dev/null || echo "")
  echo "$last" | grep -qiE "fail|error|timeout|unauthorized" && report_warn "Sync agent: $last"
  local now=$(date +%s)
  local age=$(( (now - $(stat -c %Y /tmp/gg_sync_agent.log)) / 60 ))
  [ "$age" -gt 20 ] && report_warn "Sync agent not run in ${age}min"
}

check_crons_main() {
  for c in gg_sync_agent morning_briefing; do
    sudo crontab -l 2>/dev/null | grep -q "$c" || report_critical "CRON MISSING: $c"
  done
}

# ─────────────────────────────────────────────────────────
# Layer 3: 事件分析 + spawn repair session
# ─────────────────────────────────────────────────────────

analyze_and_spawn() {
  python3 /home/airoot/.openclaw/workspace/scripts/vm/gg_log_analyzer.py 2>/dev/null || true
  
  local count=$(grep -c "CRITICAL" "$EVENTS_LOG" 2>/dev/null || echo 0)
  [ "$count" -gt 5 ] && log "⚠️ ${count} CRITICAL events in log"
  
  python3 /home/airoot/.openclaw/workspace/scripts/vm/gg_repair_spawner.py 2>/dev/null || true
}

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

{
  echo "=== Healing Cycle $(date '+%Y-%m-%d %H:%M') ($MY_HOST) ==="
  
  # Layer 1 — all machines
  check_gateway
  check_disk
  check_memory
  check_cpu
  check_network
  check_crons
  
  # Layer 2 — main only
  if $MY_IS_MAIN; then
    check_vm_tier
    check_sync_agent
    check_crons_main
  fi
  
  # Layer 3 — spawn repair session if needed
  analyze_and_spawn
  
  echo "=== Cycle Complete ==="
} >> "$HEALTH_LOG" 2>&1

tail -n 300 "$HEALTH_LOG" > "${HEALTH_LOG}.tmp" 2>/dev/null && mv "${HEALTH_LOG}.tmp" "$HEALTH_LOG" 2>/dev/null
