#!/bin/bash
# GG Dashboard — Auto data updater (cron: every 5 min)
# Generates gg-data.json for frontend to fetch

DATA_FILE="/home/airoot/.openclaw/workspace/gg-dashboard/gg-data.json"
REMINDER_STATE="/home/airoot/.openclaw/logs/gg-reminder/reminder-state.json"
CONV_LOG="/home/airoot/.openclaw/logs/conversation.jsonl"
HKT="Asia/Hong_Kong"

# Timestamp
TS=$(TZ=$HKT date +"%H:%M")
# Use %-H and %-M to avoid leading zeros (00 is invalid JSON number)
HOUR=$(TZ=$HKT date +"%-H")
MINUTE=$(TZ=$HKT date +"%-M")

# System health
CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print int($2)}')
MEM=$(free -m | awk 'NR==2{printf "%d", $3*100/$2}')
DISK=$(df / | awk 'NR==2{print int($5)}')
LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d, -f1 | tr -d ' ')
UPTIME_DAYS=$(uptime | awk '{print $3}' | tr -d ',')

# Reminders
if [ -f "$REMINDER_STATE" ]; then
  TOTAL_REM=$(python3 -c "import json; d=json.load(open('$REMINDER_STATE')); print(len(d.get('reminders',[])))" 2>/dev/null || echo "0")
  OVERDUE=$(python3 -c "
import json
d=json.load(open('$REMINDER_STATE'))
now=__import__('datetime').datetime.now()
ov=0
for r in d.get('reminders',[]):
    due=r.get('due','')
    if due:
        try:
            t=__import__('datetime').datetime.fromisoformat(due)
            if t < now: ov+=1
        except: pass
print(ov)
" 2>/dev/null || echo "0")
else
  TOTAL_REM=0
  OVERDUE=0
fi

# Today's errors from conversation log (last 24h)
ERRORS=0
if [ -f "$CONV_LOG" ]; then
  ERRORS=$(tail -200 "$CONV_LOG" 2>/dev/null | grep -ci "error\|fail\|exception" 2>/dev/null)
  ERRORS=${ERRORS:-0}
fi
ERRORS=${ERRORS//[^0-9]/}

# Service health guess
if [ -f "$REMINDER_STATE" ]; then
  if [ "$(stat -c %Y "$REMINDER_STATE" 2>/dev/null)" -gt "$(date -d '5 min ago' +%s)" ]; then
    REMINDER_STATUS="green"
  else
    REMINDER_STATUS="yellow"
  fi
else
  REMINDER_STATUS="red"
fi

DISK_STATUS="green"
[ "$DISK" -gt 85 ] && DISK_STATUS="yellow"
[ "$DISK" -gt 93 ] && DISK_STATUS="red"

MEM_STATUS="green"
[ "$MEM" -gt 80 ] && MEM_STATUS="yellow"
[ "$MEM" -gt 90 ] && MEM_STATUS="red"

# Activity log (last 5 events from conversation log)
ACTIVITY="[]"
if [ -f "$CONV_LOG" ]; then
  ACTIVITY=$(tail -20 "$CONV_LOG" 2>/dev/null | python3 -c "
import json,sys
lines=[]
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    try:
        d=json.loads(line)
        msg=d.get('message','')[:60]
        ts=d.get('timestamp','')
        if ts and msg:
            t=ts[11:16]
            lines.append({'time':t,'text':msg})
    except: pass
print(json.dumps(lines[-6:]))
" 2>/dev/null)
fi
ACTIVITY=${ACTIVITY:-[]}

# Build JSON
cat > "$DATA_FILE" << DATAEOF
{
  "ts": "$TS",
  "hour": $HOUR,
  "minute": $MINUTE,
  "system": {
    "temp": $CPU,
    "memory": $MEM,
    "disk": $DISK,
    "load": "$LOAD",
    "uptime": "$UPTIME_DAYS",
    "services": {
      "gg-reminder": "$REMINDER_STATUS",
      "disk": "$DISK_STATUS",
      "memory": "$MEM_STATUS"
    }
  },
  "reminders": {
    "total": $TOTAL_REM,
    "overdue": $OVERDUE,
    "errors": $ERRORS
  },
  "activity": $ACTIVITY
}
DATAEOF

# Maintenance data from Notion
python3 /home/airoot/.openclaw/workspace/gg-dashboard/update-maintenance.py > /home/airoot/.openclaw/workspace/gg-dashboard/gg-maintenance.json 2>/dev/null

# Memory stats from ChromaDB
python3 /home/airoot/.openclaw/workspace/gg-dashboard/update-memory-stats.py > /home/airoot/.openclaw/workspace/gg-dashboard/gg-memory-stats.json 2>/dev/null

# Count urgent maintenance items
URGENT_MAINT=$(python3 -c "import json; d=json.load(open('/home/airoot/.openclaw/workspace/gg-dashboard/gg-maintenance.json')); c=sum(1 for i in d.get('items',[]) if 'overdue' in i.get('dueStatus','') or i.get('dueStatus','').rstrip('d').isdigit() and int(i.get('dueStatus','999').rstrip('d'))<=7); print(c)" 2>/dev/null || echo "0")

echo "✅ gg-data.json updated — $TS | CPU:$CPU% MEM:${MEM}% DISK:${DISK}% REM:$TOTAL_REM MAINT:$URGENT_MAINT"

# Auto-push to DO if data changed
cd /home/airoot/.openclaw/workspace
if ! git diff --quiet gg-dashboard/gg-data.json || ! git diff --quiet gg-dashboard/gg-maintenance.json || ! git diff --quiet gg-dashboard/gg-memory-stats.json; then
  git add gg-dashboard/gg-data.json gg-dashboard/gg-maintenance.json gg-dashboard/gg-memory-stats.json
  git commit -m "G05: auto-update data ($TS)" > /dev/null 2>&1
  git push origin main > /dev/null 2>&1
  echo "🚀 Pushed to DO ($TS)"
fi
