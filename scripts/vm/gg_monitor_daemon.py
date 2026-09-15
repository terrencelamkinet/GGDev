#!/usr/bin/env python3
"""
GG Monitor Daemon — continuous health check + auto-repair
- 30s: local health (gateway, disk, memory, cpu, net)
- 60s: tunnel health + VM connectivity
- Every cycle: cron log content scan (ERROR detection) + OpenClaw journalctl
- On fail: auto-repair, log events to events.jsonl → repair_spawner pipeline
"""

import os
import sys
import json
import time
import signal
import socket
import re
import subprocess
import logging
import logging.handlers
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────
WORK_HOST = "172.6.15.181"
PERSON_HOST = "172.6.15.182"
WORK_PORT = 18901
PERSON_PORT = 18902
VM_GW_PORT = 18789
SSH_KEY = "/home/airoot/.ssh/gg_subagent"
BASE_DIR = Path("/home/airoot/.openclaw")
LOG_DIR = BASE_DIR / "logs" / "gg-v2"
EVENTS_LOG = LOG_DIR / "events.jsonl"
HEALTH_LOG = LOG_DIR / "health.log"
PID_FILE = BASE_DIR / "logs" / "gg-monitor.pid"
REPAIR_SPAWNER = str(BASE_DIR / "workspace" / "scripts" / "vm" / "gg_repair_spawner.py")

# Read gateway token
GW_TOKEN = ""
try:
    config_path = BASE_DIR / "openclaw.json"
    with open(config_path) as f:
        GW_TOKEN = json.load(f)["gateway"]["auth"]["token"]
except Exception:
    pass

MY_HOST = socket.gethostname()
IS_MAIN = MY_HOST in ("arpa-ai-test01", "gg-main")
INTERVAL_FAST = 30

# ── Logging Setup ─────────────────────────────────────
def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    lgr = logging.getLogger("gg_monitor")
    lgr.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    fh = logging.handlers.RotatingFileHandler(HEALTH_LOG, maxBytes=512*1024, backupCount=2)
    fh.setFormatter(fmt)
    lgr.addHandler(fh)
    return lgr

logger = setup_logging()

def event_id():
    return f"EVT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"

def log_event(level, category, message):
    entry = {
        "event_id": event_id(),
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": MY_HOST,
        "level": level,
        "category": category,
        "source": "gg_monitor",
        "message": message,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    with open(EVENTS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    logger.info(f"[{level}] [{category}] {message}")

# ── Helpers ───────────────────────────────────────────
def run(cmd, timeout=10, shell=True):
    try:
        r = subprocess.run(cmd if shell else cmd.split(),
                           shell=shell, capture_output=True, text=True,
                           timeout=timeout)
        return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    except Exception as e:
        return False, "", str(e)

def curl_gateway(host="127.0.0.1", port=18789, token=GW_TOKEN):
    ok, out, _ = run(
        f'curl -s --max-time 5 "http://{host}:{port}/health" '
        f'-H "Authorization: Bearer {token}"',
        timeout=8
    )
    return ok and '"ok":true' in out and '"status":"live"' in out

def percent_from_df_line(line):
    parts = line.split()
    return int(parts[4].replace('%', '')) if len(parts) >= 5 else 0

def check_vm_via_tunnel(name, host, port, token):
    ok, out, _ = run(
        f'curl -s --max-time 8 "http://127.0.0.1:{port}/health" '
        f'-H "Authorization: Bearer {token}"',
        timeout=10
    )
    return ok and '"ok":true' in out and '"status":"live"' in out

def check_vm_ssh(host):
    ok, out, _ = run(
        f'ssh -i {SSH_KEY} -o StrictHostKeyChecking=no -o ConnectTimeout=10 '
        f'airoot@{host} "echo ok"',
        timeout=12
    )
    return ok and out.strip() == "ok"

def repair_tunnels():
    logger.info("🔄 Rebuilding tunnels...")
    run("bash /home/airoot/.openclaw/workspace/gg-deploy/tunnels.sh restart", timeout=30)
    time.sleep(6)

def repair_gateway():
    logger.info("🔄 Restarting gateway...")
    run("systemctl --user restart openclaw-gateway", timeout=30)
    time.sleep(10)
    if curl_gateway():
        log_event("WARN", "healing", "Gateway restarted successfully")
        return True
    # Second attempt with node kill + restart
    logger.info("🔄 Gateway restart failed — trying node process restart...")
    run("pkill -HUP -f 'openclaw.*gateway' || kill -HUP $(pgrep -f 'openclaw.*gateway') 2>/dev/null", timeout=5)
    time.sleep(8)
    if curl_gateway():
        log_event("WARN", "healing", "Gateway restarted (HUP signal)")
        return True
    log_event("CRITICAL", "healing", "Gateway STILL DOWN after restart — repair_spawn needed")
    return False

def trigger_repair_spawn():
    """Call repair_spawner — it deduplicates and checks cooldown internally"""
    ok, out, _ = run(f"python3 {REPAIR_SPAWNER}", timeout=15)
    if ok and out:
        logger.info(f"🛠️ Repair spawner: {out[:200]}")

# Module state
STATE = {}

ERROR_PATTERNS = re.compile(
    r'\bERROR\b|Traceback \(most recent|exit code [1-9]|FAILED|Exception|'
    r'KeyError|PermissionError|ConnectionRefusedError|TimeoutError', 
    re.IGNORECASE
)

def scan_cron_logs(cron_log_files):
    """Tail last 20 lines of each cron log for ERROR patterns."""
    issues_found = False
    for logfile in cron_log_files:
        if not os.path.exists(logfile):
            log_event("WARN", "cron", f"Cron log missing: {logfile}")
            continue
        try:
            with open(logfile) as f:
                tail_lines = f.readlines()[-20:]
            for line in tail_lines:
                if ERROR_PATTERNS.search(line):
                    issues_found = True
                    meta = os.path.basename(logfile)
                    log_event("WARN", "cron", f"[{meta}] {line.strip()[:180]}")
                    break  # one WARN per log file per cycle
        except Exception as e:
            log_event("WARN", "cron", f"Failed reading {logfile}: {e}")
    return issues_found

# ── Main Loop ─────────────────────────────────────────
def run_cycle(cycle):
    """One complete health check cycle (every 30s)"""

    # ── 1. Gateway ──
    gw_ok = curl_gateway()
    if gw_ok:
        logger.debug("✅ Gateway OK")
        STATE["gw_down"] = 0
    else:
        STATE["gw_down"] = STATE.get("gw_down", 0) + 1
        if STATE["gw_down"] == 1:
            log_event("WARN", "healing", "Gateway FAIL — restarting")
            repair_gateway()
        elif STATE["gw_down"] >= 3:
            log_event("CRITICAL", "healing", "Gateway down for 90s+ — repair_spawn needed")

    # ── 2. Disk ──
    ok, out, _ = run("df / | tail -1")
    if ok:
        pct = percent_from_df_line(out)
        if pct > 90:
            log_event("CRITICAL", "system", f"Disk {pct}% — auto-cleaning")
            run("sudo journalctl --vacuum-time=3d 2>/dev/null; sudo apt-get clean 2>/dev/null")
        elif pct > 80:
            logger.warning(f"⚠️ Disk {pct}%")
        else:
            logger.debug(f"✅ Disk {pct}%")

    # ── 3. Memory ──
    try:
        with open("/proc/meminfo") as f:
            mem = f.read()
        total = int([l for l in mem.split("\n") if "MemTotal" in l][0].split()[1])
        avail = int([l for l in mem.split("\n") if "MemAvailable" in l][0].split()[1])
        pct = (total - avail) * 100 // total
        if pct > 90:
            logger.warning(f"⚠️ Memory {pct}%")
        else:
            logger.debug(f"✅ Memory {pct}%")
    except Exception:
        pass

    # ── 4. CPU load ──
    ok, out, _ = run("cat /proc/loadavg | cut -d' ' -f1")
    if ok:
        load = float(out.strip())
        cores = os.cpu_count() or 1
        pct = int((load / cores) * 100)
        if pct > 90:
            logger.warning(f"⚠️ CPU {pct}%")
        else:
            logger.debug(f"✅ CPU {pct}%")

    # ── 5. Cron heartbeat + content scan ──
    if IS_MAIN:
        cron_log_files = {
            "/tmp/daily_memory_extract.log": 28,
            "/tmp/nightly_memory_consolidation.log": 28,
            "/tmp/gg_sync_agent.log": 1,
            "/tmp/morning_briefing.log": 28,
        }
    else:
        cron_log_files = {
            "/tmp/daily_memory_extract.log": 28,
            "/tmp/nightly_memory_consolidation.log": 28,
        }

    now = time.time()
    any_cron_issue = False
    for logfile, max_hours in cron_log_files.items():
        if not os.path.exists(logfile):
            log_event("WARN", "cron", f"Cron log missing: {logfile}")
            any_cron_issue = True
            continue
        age_hours = (now - os.path.getmtime(logfile)) / 3600
        if age_hours > max_hours:
            log_event("WARN", "cron",
                      f"Cron stale: {os.path.basename(logfile)} "
                      f"not run in {age_hours:.0f}h (limit {max_hours}h)")
            any_cron_issue = True

    # Content scan: detect ERROR/traceback in cron logs
    if scan_cron_logs(list(cron_log_files.keys())):
        any_cron_issue = True

    # ── 6. OpenClaw journalctl — message timeout / connection errors ──
    ok, out, _ = run(
        "journalctl --user -u openclaw --since '10 min ago' --no-pager -n 50 2>/dev/null "
        "| grep -iE 'timeout|fail|error|retry|provider|connection' | tail -5"
    )
    if ok and out:
        for line in out.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            if "timeout" in line.lower():
                log_event("WARN", "message", f"Message timeout: {line[:120]}")
                any_cron_issue = True
            elif any(x in line.lower() for x in ["fail", "error"]):
                log_event("WARN", "gateway", f"Gateway error: {line[:120]}")
                any_cron_issue = True

    # ── 7. Network ──
    ok, _, _ = run("dig +short google.com @8.8.8.8 2>/dev/null | head -1")
    if not ok:
        log_event("WARN", "network", "DNS/network failure — auto-repairing")
        run("sudo dhclient -v 2>/dev/null", timeout=20)
        any_cron_issue = True
    else:
        logger.debug("✅ Network OK")

    # ── 8. If any issue found, trigger repair spawner ──
    if any_cron_issue:
        trigger_repair_spawn()

    # ── 9. VM / Tunnel checks (every 2nd cycle = 60s, main only) ──
    if cycle % 2 == 0 and IS_MAIN:
        # Tunnel ports
        ok, out, _ = run("ss -tlnp | grep -E '18901|18902'")
        if ok:
            logger.debug("✅ Tunnel ports OK")
        else:
            log_event("WARN", "tunnel", "Tunnel ports down — rebuilding")
            repair_tunnels()

        # VM via tunnels
        work_ok = check_vm_via_tunnel("work", WORK_HOST, WORK_PORT,
            "bf80e73561d252ec9345a2be8be7c4c0e952187ef0d4f375202a62de1b3cf8a2")
        person_ok = check_vm_via_tunnel("person", PERSON_HOST, PERSON_PORT,
            "49ccb297fe1533acf64b4d8925713782be2d58f9b68eb34cdcd50a761473b652")

        if work_ok:
            logger.debug("✅ GG-Work via tunnel")
        else:
            logger.warning("❌ GG-Work tunnel fail")
            if check_vm_ssh(WORK_HOST):
                log_event("WARN", "tunnel", "Work VM OK (SSH) but tunnel broken")
                repair_tunnels()
            else:
                log_event("CRITICAL", "vm", "Work VM OFFLINE (SSH fail)")

        if person_ok:
            logger.debug("✅ GG-Person via tunnel")
        else:
            logger.warning("❌ GG-Person tunnel fail")
            if check_vm_ssh(PERSON_HOST):
                log_event("WARN", "tunnel", "Person VM OK (SSH) but tunnel broken")
                repair_tunnels()
            else:
                log_event("CRITICAL", "vm", "Person VM OFFLINE (SSH fail)")

        # Rebuild if both down
        if not work_ok and not person_ok:
            log_event("CRITICAL", "tunnel", "Both VMs unreachable — rebuilding tunnels")
            repair_tunnels()

        # VM tunnel issues → also trigger repair spawner
        if not work_ok or not person_ok:
            trigger_repair_spawn()


def main():
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    logger.info(f"🚀 GG Monitor Daemon started (PID {os.getpid()}, main={IS_MAIN})")

    cycle = 0
    try:
        while True:
            run_cycle(cycle)
            cycle += 1
            time.sleep(INTERVAL_FAST)
    except KeyboardInterrupt:
        logger.info("🛑 Monitor stopped by signal")
    finally:
        PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
