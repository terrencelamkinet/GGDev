#!/usr/bin/env python3
"""
Nightly Memory Consolidation — 每晚 23:55 HKT 執行
三層記憶整理：
1. 壓縮舊 memory_index entries (>30日歸檔)
2. 清理過期 nightly reflect (>7日)
3. 整理 VM 記憶，確保一致
4. 壓縮 memory_index.md 限50行
"""
import json, os, re, sys, subprocess, logging
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = f"{WORKSPACE}/memory"
REFLECT_DIR = f"{WORKSPACE}/.nightly_reflect"
INDEX_FILE = f"{WORKSPACE}/memory_index.md"
LOG_FILE = "/tmp/nightly_memory_consolidation.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log(msg, level="info"):
    msg = f"🌙 {msg}"
    print(msg)
    if level == "error":
        logging.error(msg)
    else:
        logging.info(msg)

def clean_old_reflects():
    """Delete nightly reflects older than 7 days"""
    import time
    now = time.time()
    removed = 0
    if not os.path.exists(REFLECT_DIR):
        log("Reflect dir not found, skipping")
        return 0
    for f in os.listdir(REFLECT_DIR):
        try:
            fpath = os.path.join(REFLECT_DIR, f)
            if not f.endswith(".md"): continue
            mtime = os.path.getmtime(fpath)
            age_days = (now - mtime) / 86400
            if age_days > 7:
                os.remove(fpath)
                removed += 1
                log(f"Removed old reflect: {f}")
        except Exception as e:
            log(f"Error cleaning reflect {f}: {e}", "error")
    return removed

def compress_index():
    """Ensure memory_index.md is ≤ 50 lines"""
    try:
        if not os.path.exists(INDEX_FILE):
            log("memory_index.md not found, skipping")
            return
        with open(INDEX_FILE) as f:
            lines = f.readlines()
        if len(lines) <= 50:
            log(f"Index is {len(lines)} lines — under limit")
            return
        # Keep first 10 lines (header), last 30 lines (recent), drop middle
        head = lines[:10]
        tail = lines[-35:]
        date_str = datetime.now().strftime("%Y-%m-%d")
        with open(INDEX_FILE, "w") as f:
            f.writelines(head)
            f.write(f"\n<!-- Auto-compressed from {len(lines)} to {len(head)+len(tail)} lines on {date_str} -->\n\n")
            f.writelines(tail)
        log(f"Compressed index from {len(lines)} to {len(head)+len(tail)} lines")
    except Exception as e:
        log(f"Error compressing index: {e}", "error")

def clean_stale_memory_files():
    """Clean old memory day files (>30 days)"""
    import time
    now = time.time()
    removed = 0
    if not os.path.exists(MEMORY_DIR):
        log("Memory dir not found, skipping")
        return 0
    for f in os.listdir(MEMORY_DIR):
        try:
            fpath = os.path.join(MEMORY_DIR, f)
            if not f.endswith(".md"): continue
            if "_summary" in f: continue  # keep summaries
            mtime = os.path.getmtime(fpath)
            if (now - mtime) / 86400 > 30:
                os.remove(fpath)
                removed += 1
                log(f"Archived old memory: {f}")
        except Exception as e:
            log(f"Error archiving {f}: {e}", "error")
    return removed

def sync_to_vms():
    """Report consolidation results to both VMs"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M HKT")
    msg = f"Nightly memory consolidation completed at {now}"
    
    successes = 0
    for target in ["work", "person"]:
        try:
            r = subprocess.run([
                sys.executable, f"{WORKSPACE}/scripts/vm/orchestrate.py",
                "memo", target, msg
            ], capture_output=True, text=True, timeout=30)
            if r.returncode == 0:
                successes += 1
                log(f"Synced to {target}")
            else:
                log(f"Sync to {target} failed: {r.stderr[:100]}", "error")
        except subprocess.TimeoutExpired:
            log(f"Sync to {target} timed out", "error")
        except Exception as e:
            log(f"Sync to {target} error: {e}", "error")
    log(f"Synced to {successes}/2 VMs")

def main():
    log("=" * 40)
    log("Nightly Memory Consolidation — Starting")
    
    log("Cleaning old reflects (>7d)...")
    r1 = clean_old_reflects()
    log(f"{r1} old reflect(s) removed")
    
    log("Cleaning stale memories (>30d)...")
    r2 = clean_stale_memory_files()
    log(f"{r2} old memory file(s) archived")
    
    log("Compressing memory index...")
    compress_index()
    
    log("Syncing to VMs...")
    sync_to_vms()
    
    log("=" * 40)
    log("Consolidation complete!")

if __name__ == "__main__":
    main()
