#!/usr/bin/env python3
"""
GG Auto-Log Wrapper — 自動記錄所有操作

用法: 每次做完任何操作後，用呢個 script 記錄

Categories:
  conversation — 對話重點
  upgrade — 系統升級/更新
  communication — 跨機溝通/通知
  connection — tunnel/SSH/network 狀態
  cron — cron job 執行
  error — 錯誤
  config — 配置改動
  command — 執行嘅命令
"""
import json, os, sys, subprocess, argparse
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
SCRIPT_DIR = os.path.join(WORKSPACE, "scripts/vm")

def log_locally(category, content, level="info"):
    """Log to local JSONL + daily memory file"""
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H:%M:%S")
    
    # JSONL log
    log_dir = os.path.expanduser("~/.openclaw/logs/gg")
    os.makedirs(log_dir, exist_ok=True)
    entry = {
        "ts": f"{today}T{ts}",
        "host": os.uname().nodename,
        "level": level.upper(),
        "category": category,
        "message": content[:500]
    }
    with open(os.path.join(log_dir, "auto.log"), "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    # Daily memory file (append)
    os.makedirs(MEMORY_DIR, exist_ok=True)
    mem_file = os.path.join(MEMORY_DIR, f"{today}.md")
    ts_hkt = datetime.now().strftime("%H:%M HKT")
    
    cat_emoji = {
        "conversation": "💬",
        "upgrade": "⬆️",
        "communication": "📡",
        "connection": "🔗",
        "cron": "⏰",
        "error": "❌",
        "config": "⚙️",
        "command": "⌨️",
        "system": "🖥️",
        "memory": "🧠",
        "backup": "💾"
    }.get(category, "📝")
    
    line = f"\n- **{ts_hkt}** {cat_emoji} **[{category.upper()}]** {content}"
    
    # Check if file exists, create header if not
    if not os.path.exists(mem_file):
        with open(mem_file, "w") as f:
            f.write(f"# {today}\n")
    
    with open(mem_file, "a") as f:
        f.write(line)

def sync_to_vms(category, content):
    """Sync log to GG-Work and GG-Person VMs"""
    for target in ["work", "person"]:
        try:
            subprocess.run([
                sys.executable, os.path.join(SCRIPT_DIR, "orchestrate.py"),
                "memo", target, f"[{category.upper()}] {content[:200]}"
            ], capture_output=True, timeout=30)
        except Exception:
            pass  # Don't fail if sync fails

def main():
    parser = argparse.ArgumentParser(description="GG Auto-Log")
    parser.add_argument("category", 
                       choices=["conversation","upgrade","communication","connection",
                                "cron","error","config","command","system","memory","backup"],
                       help="log category")
    parser.add_argument("content", help="what happened")
    parser.add_argument("--no-sync", action="store_true", help="skip VM sync")
    parser.add_argument("--level", choices=["info","warn","error"], default="info")
    parser.add_argument("--details", help="optional JSON details")
    
    args = parser.parse_args()
    
    # Log locally
    log_locally(args.category, args.content, args.level)
    
    # Sync to VMs (unless --no-sync)
    if not args.no_sync:
        sync_to_vms(args.category, args.content)
    
    result = {"ok": True, "category": args.category, "logged": True}
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
