#!/bin/bash
# Tunnel Manager for GG Sub-agent VMs
# Maintains SSH tunnels from main GG to work/person VM gateways

WORK_PID_FILE="/home/airoot/.openclaw/logs/gg-v2/work_tunnel.pid"
PERSON_PID_FILE="/home/airoot/.openclaw/logs/gg-v2/person_tunnel.pid"
WORK_HOST="172.6.15.181"
PERSON_HOST="172.6.15.182"
WORK_PORT=18901
PERSON_PORT=18902
VM_GW_PORT=18789
SSH_KEY="/home/airoot/.ssh/gg_subagent"

status() {
    echo "🔍 Checking tunnel status..."
    
    if [ -f "$WORK_PID_FILE" ] && kill -0 $(cat "$WORK_PID_FILE") 2>/dev/null; then
        echo "✅ work tunnel — ACTIVE (PID $(cat $WORK_PID_FILE))"
    else
        echo "❌ work tunnel — STOPPED (stale PID)"
    fi
    
    if [ -f "$PERSON_PID_FILE" ] && kill -0 $(cat "$PERSON_PID_FILE") 2>/dev/null; then
        echo "✅ person tunnel — ACTIVE (PID $(cat $PERSON_PID_FILE))"
    else
        echo "❌ person tunnel — STOPPED (stale PID)"
    fi
    
    echo ""
    echo "Port check:"
    ss -tlnp | grep -E "$WORK_PORT|$PERSON_PORT" | sed 's/^/  /'
}

start() {
    echo "🚀 Starting tunnels..."
    
    # Kill existing by port, not PID files (avoids permission issues)
    for p in $WORK_PORT $PERSON_PORT; do
        OLD_PID=$(ss -tlnp | grep ":$p " | grep -oP 'pid=\K[0-9]+' | head -1)
        [ -n "$OLD_PID" ] && kill $OLD_PID 2>/dev/null && echo "  Killed old tunnel on port $p (PID $OLD_PID)" || true
    done
    sleep 1
    
    # Work tunnel
    ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
        -fNL ${WORK_PORT}:127.0.0.1:${VM_GW_PORT} airoot@${WORK_HOST} sleep 99999
    sleep 2
    WORK_PID=$(ss -tlnp | grep ":$WORK_PORT " | grep -oP 'pid=\K[0-9]+' | head -1)
    echo "$WORK_PID" > "$WORK_PID_FILE" 2>/dev/null || true
    echo "  ✅ work tunnel → localhost:$WORK_PORT (PID $WORK_PID)"
    
    # Person tunnel
    ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
        -fNL ${PERSON_PORT}:127.0.0.1:${VM_GW_PORT} airoot@${PERSON_HOST} sleep 99999
    sleep 2
    PERSON_PID=$(ss -tlnp | grep ":$PERSON_PORT " | grep -oP 'pid=\K[0-9]+' | head -1)
    echo "$PERSON_PID" > "$PERSON_PID_FILE" 2>/dev/null || true
    echo "  ✅ person tunnel → localhost:$PERSON_PORT (PID $PERSON_PID)"
}

stop() {
    echo "🛑 Stopping tunnels..."
    [ -f "$WORK_PID_FILE" ] && kill $(cat "$WORK_PID_FILE") 2>/dev/null && echo "  ✅ work tunnel stopped" || true
    [ -f "$PERSON_PID_FILE" ] && kill $(cat "$PERSON_PID_FILE") 2>/dev/null && echo "  ✅ person tunnel stopped" || true
    rm -f "$WORK_PID_FILE" "$PERSON_PID_FILE"
}

case "${1:-status}" in
    start) start ;;
    stop)  stop  ;;
    restart) stop; sleep 1; start ;;
    status|*) status ;;
esac
