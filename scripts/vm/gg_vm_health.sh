#!/bin/bash
# GG VM Health — 自治健康檢測（每5分鐘）
# 每部VM獨立執行，不需主機參與
HEALTH_LOG="/home/airoot/.openclaw/logs/gg-v2/health.log"
MY_HOST=$(hostname)

# 自動偵測 token（從 gateway config）
TOKEN=$(python3 -c "
import json
try:
    print(json.load(open('/home/airoot/.openclaw/openclaw.json'))['gateway']['auth']['token'])
except:
    print('')
" 2>/dev/null)

API_URL="http://127.0.0.1:18789/v1/chat/completions"

log() { echo "[$(date '+%H:%M:%S')] $*" >> "$HEALTH_LOG"; }

report_issue() {
  local level="$1" msg="$2"
  log "$level $msg"
  # Write to events.jsonl for sync agent to pick up
  python3 -c "
import json, os
evt = {
    'event_id': 'EVT-$(date +%Y%m%d-%H%M%S)',
    'ts': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'host': '$MY_HOST',
    'level': '$level',
    'category': 'health',
    'source': 'auto_repair',
    'message': '$msg',
    'date': '$(date +%Y-%m-%d)'
}
path = '/home/airoot/.openclaw/logs/gg-v2/events.jsonl'
with open(path, 'a') as f:
    f.write(json.dumps(evt) + '\n')
" 2>/dev/null || true
}

{
  echo "=== Health Check $(date '+%Y-%m-%d %H:%M') ($MY_HOST) ==="
  
  if [ -z "$TOKEN" ]; then
    log "🔴 Cannot find gateway token"
    echo "=== Done ==="
    exit 1
  fi
  
  # ── 1. OpenClaw Gateway 檢測 ──
  result=$(curl -s --max-time 15 "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"messages":[{"role":"user","content":"ping"}]}' 2>&1)
  
  if echo "$result" | grep -q '"finish_reason":"stop"'; then
    log "✅ OpenClaw gateway OK"
  else
    log "❌ OpenClaw gateway FAIL"
    report_issue "🔴" "OpenClaw gateway FAIL - restarting"
    # Try restart
    systemctl --user restart openclaw 2>/dev/null || true
    sleep 10
    result2=$(curl -s --max-time 15 "$API_URL" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{"messages":[{"role":"user","content":"ping"}]}' 2>&1)
    if echo "$result2" | grep -q '"finish_reason":"stop"'; then
      log "  ✅ OpenClaw restarted OK"
    else
      log "  🔴 OpenClaw STILL DOWN — CRITICAL"
      report_issue "CRITICAL" "OpenClaw gateway down on $MY_HOST after restart attempt"
    fi
  fi
  
  # ── 2. Disk Space ──
  usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
  if [ "$usage" -gt 90 ]; then
    log "🔴 CRITICAL: Disk ${usage}%"
    report_issue "🔴" "CRITICAL disk usage: ${usage}% on $MY_HOST"
  elif [ "$usage" -gt 80 ]; then
    log "⚠️ WARNING: Disk ${usage}%"
  else
    log "✅ Disk ${usage}%"
  fi
  
  # ── 3. Memory / CPU (quick check) ──
  mem_pct=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
  if [ "$mem_pct" -gt 90 ]; then
    log "🔴 Memory ${mem_pct}%"
    report_issue "🔴" "High memory: ${mem_pct}% on $MY_HOST"
  elif [ "$mem_pct" -gt 80 ]; then
    log "⚠️ Memory ${mem_pct}%"
  else
    log "✅ Memory ${mem_pct}%"
  fi
  
  # ── 4. Cron heartbeat — check if log files are recent ──
  now=$(date +%s)
  for logfile in /tmp/daily_memory_extract.log /tmp/nightly_memory_consolidation.log; do
    if [ -f "$logfile" ]; then
      age_h=$(( (now - $(stat -c %Y "$logfile" 2>/dev/null || echo 0)) / 3600 ))
      if [ $age_h -gt 28 ]; then
        log "⚠️ $(basename $logfile) stale (${age_h}h ago)"
        report_issue "⚠️" "Cron $(basename $logfile) stale on $MY_HOST (${age_h}h)"
      fi
    fi
  done
  
  echo "=== Done ==="
} >> "$HEALTH_LOG" 2>&1

# Trim log (last 200 lines)
tail -n 200 "$HEALTH_LOG" > "${HEALTH_LOG}.tmp" 2>/dev/null && mv "${HEALTH_LOG}.tmp" "$HEALTH_LOG" 2>/dev/null
