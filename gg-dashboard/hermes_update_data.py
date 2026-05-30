#!/usr/bin/env python3
"""Hermes Dashboard Data Updater — collects health data from all 3 machines."""
import json, os, subprocess
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
DATA_DIR = os.path.expanduser("~/projects/ggdev-repo/gg-dashboard")
DATA_FILE = os.path.join(DATA_DIR, "gg-data.json")


def run_cmd(cmd_list, timeout=10):
    try:
        r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""


def ssh(host, remote_cmd, timeout=10):
    """Run a command on remote host via SSH alias."""
    cmd_list = ["ssh", "-o", "ConnectTimeout=5", host] + remote_cmd
    try:
        r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""


def poll_machine(name, host=""):
    """Poll a machine for system stats. Empty host = local (Main)."""
    if host:
        top_raw = ssh(host, ["top", "-bn1"])
        free_raw = ssh(host, ["free", "-m"])
        df_raw = ssh(host, ["df", "/"])
        uptime_raw = ssh(host, ["uptime", "-p"])
        load_raw = ssh(host, ["uptime"])
        reminder_pid = ssh(host, ["pgrep", "-f", "gg_reminder_daemon"])
        monitor_pid = ssh(host, ["pgrep", "-f", "gg_monitor_daemon"])
        openclaw_pid = ssh(host, ["pgrep", "-f", "openclaw"])
    else:
        top_raw = run_cmd(["top", "-bn1"])
        free_raw = run_cmd(["free", "-m"])
        df_raw = run_cmd(["df", "/"])
        uptime_raw = run_cmd(["uptime", "-p"])
        load_raw = run_cmd(["uptime"])
        reminder_pid = run_cmd(["pgrep", "-f", "gg_reminder_daemon"])
        monitor_pid = run_cmd(["pgrep", "-f", "gg_monitor_daemon"])
        openclaw_pid = run_cmd(["pgrep", "-f", "openclaw"])

    # Parse CPU from top output
    cpu = 0
    for line in top_raw.split("\n"):
        if "%Cpu(s)" in line or "Cpu(s)" in line:
            parts = line.split(",")
            for p in parts:
                p = p.strip()
                if "id" in p:
                    try:
                        idle = float(p.split()[0])
                        cpu = max(0, int(100 - idle))
                    except:
                        cpu = 0
                    break

    # Parse MEM from free output
    mem = 0
    for line in free_raw.split("\n"):
        if line.startswith("Mem:"):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    total = float(parts[1])
                    used = float(parts[2])
                    mem = int(used * 100 / total) if total > 0 else 0
                except:
                    mem = 0
            break

    # Parse DISK from df output
    disk = 0
    for line in df_raw.split("\n"):
        if line.startswith("/"):
            parts = line.split()
            if len(parts) >= 5:
                try:
                    disk = int(parts[4].replace("%", ""))
                except:
                    disk = 0
            break

    # Parse uptime
    uptime = uptime_raw.replace("up ", "").strip() if uptime_raw else "?"
    # Parse load
    load = "0"
    for line in load_raw.split("\n"):
        if "load average:" in line:
            load = line.split("load average:")[-1].split(",")[0].strip()
            break

    return {
        "cpu": cpu,
        "mem": mem,
        "disk": disk,
        "uptime": uptime,
        "load": load or "0",
        "daemons": {
            "reminder": bool(reminder_pid),
            "monitor": bool(monitor_pid),
            "openclaw": bool(openclaw_pid),
        },
        "online": bool(cpu or mem or disk),
    }


def get_agent_activity():
    """Get recent cron job activity from logs."""
    log_dir = os.path.expanduser("~/.hermes/logs")
    activity = []
    if os.path.isdir(log_dir):
        logs = sorted(os.listdir(log_dir), reverse=True)[:10]
        for log in logs:
            log_path = os.path.join(log_dir, log)
            if os.path.isfile(log_path):
                mtime = datetime.fromtimestamp(os.path.getmtime(log_path), tz=HKT)
                fsize = os.path.getsize(log_path)
                activity.append({
                    "time": mtime.strftime("%H:%M"),
                    "text": f"Cron: {log[:50]} ({fsize}B)",
                })
    now = datetime.now(HKT)
    activity.insert(0, {"time": now.strftime("%H:%M"), "text": "Dashboard data refresh"})
    return activity[:10]


def get_cron_info():
    """Count active cron jobs."""
    try:
        r = run_cmd(["hermes", "cron", "list"])
        if r:
            data = json.loads(r)
            if isinstance(data, list):
                return len([c for c in data if c.get("schedule")])
    except:
        pass
    return 12


def main():
    now = datetime.now(HKT)
    ts = now.strftime("%H:%M")
    hour = now.hour
    minute = now.minute

    main_stats = poll_machine("Main")
    work_stats = poll_machine("GG-Work", "gg-work")
    person_stats = poll_machine("GG-Person", "gg-person")

    all_online = main_stats["online"] and work_stats["online"] and person_stats["online"]
    has_issues = (
        main_stats["mem"] > 80
        or main_stats["disk"] > 90
        or work_stats["mem"] > 80
        or work_stats["disk"] > 90
        or person_stats["mem"] > 80
        or person_stats["disk"] > 90
    )

    if not all_online:
        badge_color = "red"
        badge_text = "● Offline"
    elif has_issues:
        badge_color = "yellow"
        badge_text = "● Warning"
    else:
        badge_color = "green"
        badge_text = "● All OK"

    data = {
        "ts": ts,
        "hour": hour,
        "minute": minute,
        "system": {
            "temp": main_stats["cpu"],
            "memory": main_stats["mem"],
            "disk": main_stats["disk"],
            "load": main_stats["load"],
            "uptime": main_stats["uptime"],
            "services": {
                "gg-reminder": "green" if work_stats["daemons"]["reminder"] else "red",
                "disk": "green" if main_stats["disk"] < 90 else ("yellow" if main_stats["disk"] < 95 else "red"),
                "memory": "green" if main_stats["mem"] < 80 else ("yellow" if main_stats["mem"] < 90 else "red"),
            },
        },
        "reminders": {"total": 20, "overdue": 0, "errors": 0},
        "activity": get_agent_activity(),
        "agents": {
            "main": {
                "cpu": main_stats["cpu"],
                "mem": main_stats["mem"],
                "disk": main_stats["disk"],
                "load": main_stats["load"],
                "uptime": main_stats["uptime"],
                "daemons": main_stats["daemons"],
                "online": main_stats["online"],
                "cron_jobs": get_cron_info(),
            },
            "work": {
                "cpu": work_stats["cpu"],
                "mem": work_stats["mem"],
                "disk": work_stats["disk"],
                "load": work_stats["load"],
                "uptime": work_stats["uptime"],
                "daemons": work_stats["daemons"],
                "online": work_stats["online"],
                "ip": "172.6.15.181",
            },
            "person": {
                "cpu": person_stats["cpu"],
                "mem": person_stats["mem"],
                "disk": person_stats["disk"],
                "load": person_stats["load"],
                "uptime": person_stats["uptime"],
                "daemons": person_stats["daemons"],
                "online": person_stats["online"],
                "ip": "172.6.15.182",
            },
        },
        "badge_color": badge_color,
        "badge_text": badge_text,
        "update_source": "hermes_update_data.py",
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(
        f"✅ gg-data.json updated — {ts}"
        f" | Main:{'✓' if main_stats['online'] else '✗'}"
        f" Work:{'✓' if work_stats['online'] else '✗'}"
        f" Person:{'✓' if person_stats['online'] else '✗'}"
    )


if __name__ == "__main__":
    main()
