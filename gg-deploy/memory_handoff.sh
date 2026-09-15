#!/bin/bash
# memory_handoff.sh — 將 GG 大總管嘅 knowledge 注入 sub-agent
# 由 GG 大總管 call exec 透過 SSH 執行

ACTION="$1"
AGENT_IP="$2"
SSH_PASS='1@2B3c444$'
SSH_CMD="sshpass -p $SSH_PASS ssh -o StrictHostKeyChecking=no airoot@$AGENT_IP"

case "$ACTION" in
  create-dirs)
    $SSH_CMD "mkdir -p ~/gg{,-work,-person}/{,.openclaw} memory skills projects"
    ;;
  
  deploy-soul)
    # 部署 SOUL.md
    $SSH_CMD "cat > ~/gg/SOUL.md" < /home/airoot/.openclaw/workspace/gg-deploy/SOUL_TEMPLATE.md
    ;;
  
  deploy-profile)
    # 部署 profile
    $SSH_CMD "cat > ~/gg/PROFILE.md" 
    ;;
  
  install-skills)
    # Install skills from clawhub
    $SSH_CMD "cd ~/gg && npm init -y 2>/dev/null; clawhub install hko-weather 2>/dev/null; clawhub install hko-rain 2>/dev/null; clawhub install kmb-eta 2>/dev/null; clawhub install citybus-eta 2>/dev/null; clawhub install mtr-eta 2>/dev/null; clawhub install hk-public-holidays 2>/dev/null"
    ;;
  
  test)
    $SSH_CMD "openclaw status 2>&1 | head -15"
    ;;
  
  *)
    echo "Usage: $0 {create-dirs|deploy-soul|deploy-profile|install-skills|test} <ip>"
    exit 1
    ;;
esac
