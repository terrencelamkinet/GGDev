#!/usr/bin/env python3
"""Hermes Dashboard Data Updater — collects health data from all 3 machines.
Preserves costs, agent thoughts/needs/learnings/uncertainties, schedule, pushed_at."""
import json, os, subprocess
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
DATA_DIR = os.path.expanduser("~/projects/ggdev-repo/gg-dashboard")
DATA_FILE = os.path.join(DATA_DIR, "gg-data.json")
COST_FILE = os.path.expanduser("~/.hermes/cost_history.json")

# Agent thoughts — fallback defaults (overwritten by merge_preserved from existing file)
DEFAULT_THOUGHTS = {
    "main": {
        "thoughts": "Monitoring system health across all 3 VMs. Ready to assist.",
        "needs": ["None at this time"],
        "learnings": ["Dashboard data pipeline fixed", "Focus Bird v2.0 deployed"],
        "uncertainties": ["BrainLink latency under real usage"],
    },
    "work": {
        "thoughts": "Dashboard data collection and system monitoring running on schedule.",
        "needs": ["None urgent"],
        "learnings": ["SSH health polling working across all VMs"],
        "uncertainties": ["None"],
    },
    "person": {
        "thoughts": "Ready to manage personal tasks, reminders, and schedule.",
        "needs": ["None urgent"],
        "learnings": ["Personal task pipeline stable"],
        "uncertainties": ["None"],
    },
}


def run_cmd(cmd_list, timeout=10):
    try:
        r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""


def ssh(host, remote_cmd, timeout=10):
    cmd_list = ["ssh", "-o", "ConnectTimeout=5", host] + remote_cmd
    try:
        r = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""


def poll_machine(name, host=""):
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

    uptime = uptime_raw.replace("up ", "").strip() if uptime_raw else "?"
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
    log_dir = os.path.expanduser("~/.hermes/logs")
    activity = []
    if os.path.isdir(log_dir):
        logs = sorted(os.listdir(log_dir), reverse=True)[:10]
        for log in logs:
            log_path = os.path.join(log_dir, log)
            if os.path.isfile(log_path):
                mtime = datetime.fromtimestamp(os.path.getmtime(log_path), tz=HKT)
                fsize = os.path.getsize(log_path)
                activity.append({"time": mtime.strftime("%H:%M"), "text": f"Cron: {log[:50]} ({fsize}B)"})
    now = datetime.now(HKT)
    activity.insert(0, {"time": now.strftime("%H:%M"), "text": "Dashboard data refresh"})
    return activity[:10]


def get_cron_info():
    try:
        r = run_cmd(["hermes", "cron", "list"])
        if r:
            data = json.loads(r)
            if isinstance(data, list):
                return len([c for c in data if c.get("schedule")])
    except:
        pass
    return 12


def build_costs():
    """Build costs structure from cost_history.json."""
    if not os.path.exists(COST_FILE):
        return {}
    try:
        cost_data = json.load(open(COST_FILE))
    except:
        return {}

    days = cost_data.get("days", {})
    daily_list = [(date, v) for date, v in days.items() if isinstance(v, dict)]
    daily_list.sort(key=lambda x: x[0], reverse=True)

    total_7d = sum(v.get("total", {}).get("cost", 0) for _, v in daily_list[:7])
    sess_7d = sum(v.get("total", {}).get("sessions", 0) for _, v in daily_list[:7])
    tok_7d = sum(v.get("total", {}).get("tokens", 0) for _, v in daily_list[:7])

    total_30d = sum(v.get("total", {}).get("cost", 0) for _, v in daily_list[:30])
    sess_30d = sum(v.get("total", {}).get("sessions", 0) for _, v in daily_list[:30])
    tok_30d = sum(v.get("total", {}).get("tokens", 0) for _, v in daily_list[:30])

    now = datetime.now(HKT)
    month_key = now.strftime("%Y-%m")
    month_data = cost_data.get("months", {}).get(month_key, {})

    return {
        "summary": {
            "7d": {"cost": round(total_7d, 4), "sessions": sess_7d, "tokens": tok_7d},
            "30d": {"cost": round(total_30d, 4), "sessions": sess_30d, "tokens": tok_30d},
            "month": {
                "cost": round(month_data.get("total", {}).get("cost", total_30d), 4),
                "sessions": month_data.get("total", {}).get("sessions", sess_30d),
                "tokens": month_data.get("total", {}).get("tokens", tok_30d),
            },
        },
        "daily": [
            {
                "date": date,
                "cost": round(v.get("total", {}).get("cost", 0), 4),
                "sessions": v.get("total", {}).get("sessions", 0),
                "tokens": v.get("total", {}).get("tokens", 0),
            }
            for date, v in daily_list[:30]
        ],
        "monthly": [
            {"date": mk, "cost": round(mv.get("total", {}).get("cost", 0), 4),
             "sessions": mv.get("total", {}).get("sessions", 0),
             "tokens": mv.get("total", {}).get("tokens", 0)}
            for mk, mv in cost_data.get("months", {}).items()
        ],
        "providers_30d": {
            "deepseek": {"sessions": sess_30d, "tokens": tok_30d, "cost": round(total_30d, 4)}
        },
        "balance": None,
    }


def merge_preserved(existing, new_data):
    """Preserve fields from existing file that aren't in the new data."""
    if existing is None:
        return new_data

    # Preserve costs
    if existing.get("costs"):
        new_data["costs"] = existing["costs"]

    # Preserve schedule
    if existing.get("schedule"):
        new_data["schedule"] = existing["schedule"]

    # Preserve pushed_at (override with current time later)
    if existing.get("pushed_at"):
        new_data["pushed_at"] = existing["pushed_at"]

    # Preserve agent introspection fields
    if "agents" in existing:
        for agent_key in ["main", "work", "person"]:
            if agent_key in existing["agents"] and agent_key in new_data["agents"]:
                ea = existing["agents"][agent_key] or {}
                na = new_data["agents"][agent_key]
                for field in ["thoughts", "needs", "learnings", "uncertainties"]:
                    if field in ea and ea[field]:
                        na[field] = ea[field]
                    elif field not in na:
                        # Inject from defaults
                        na[field] = DEFAULT_THOUGHTS.get(agent_key, {}).get(field)
                # Preserve non-overwritten fields
                for field in ["ip", "cron_jobs"]:
                    if field in ea:
                        na[field] = ea[field]

    return new_data


def main():
    now = datetime.now(HKT)
    ts = now.strftime("%H:%M")
    hour = now.hour
    minute = now.minute
    pushed_at = now.strftime("%Y-%m-%d %H:%M HKT")

    # Read existing data first
    existing = None
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                existing = json.load(f)
        except:
            existing = None

    main_stats = poll_machine("Main")
    work_stats = poll_machine("GG-Work", "gg-work")
    person_stats = poll_machine("GG-Person", "gg-person")

    all_online = main_stats["online"] and work_stats["online"] and person_stats["online"]
    has_issues = (
        main_stats["mem"] > 80 or main_stats["disk"] > 90
        or work_stats["mem"] > 80 or work_stats["disk"] > 90
        or person_stats["mem"] > 80 or person_stats["disk"] > 90
    )

    if not all_online:
        badge_color, badge_text = "red", "● Offline"
    elif has_issues:
        badge_color, badge_text = "yellow", "● Warning"
    else:
        badge_color, badge_text = "green", "● All OK"

    data = {
        "ts": ts,
        "hour": hour,
        "minute": minute,
        "pushed_at": pushed_at,
        "system": {
            "cpu": main_stats["cpu"],
            "mem": main_stats["mem"],
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
                "cpu": main_stats["cpu"], "mem": main_stats["mem"],
                "disk": main_stats["disk"], "load": main_stats["load"],
                "uptime": main_stats["uptime"],
                "daemons": main_stats["daemons"], "online": main_stats["online"],
                "cron_jobs": get_cron_info(),
            },
            "work": {
                "cpu": work_stats["cpu"], "mem": work_stats["mem"],
                "disk": work_stats["disk"], "load": work_stats["load"],
                "uptime": work_stats["uptime"],
                "daemons": work_stats["daemons"], "online": work_stats["online"],
                "ip": "172.6.15.181",
            },
            "person": {
                "cpu": person_stats["cpu"], "mem": person_stats["mem"],
                "disk": person_stats["disk"], "load": person_stats["load"],
                "uptime": person_stats["uptime"],
                "daemons": person_stats["daemons"], "online": person_stats["online"],
                "ip": "172.6.15.182",
            },
        },
        "badge_color": badge_color,
        "badge_text": badge_text,
        "costs": build_costs(),
        "schedule": existing.get("schedule", []) if existing else [],
        "update_source": "hermes_update_data.py",
    }

    # Merge preserved fields and agent introspection
    data = merge_preserved(existing, data)

    os.makedirs(DATA_DIR, exist_ok=True)
    # Atomic write: temp file + rename
    import tempfile
    tmp = tempfile.NamedTemporaryFile(
        mode='w', dir=DATA_DIR, prefix='.tmp-', suffix='.json',
        delete=False, encoding='utf-8'
    )
    try:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.close()
        os.replace(tmp.name, DATA_FILE)
    except:
        os.unlink(tmp.name)
        raise

    print(
        f"✅ gg-data.json updated — {ts}"
        f" | Main:{'✓' if main_stats['online'] else '✗'}"
        f" Work:{'✓' if work_stats['online'] else '✗'}"
        f" Person:{'✓' if person_stats['online'] else '✗'}"
        f" | Costs: ${data.get('costs',{}).get('summary',{}).get('7d',{}).get('cost',0)}"
    )


if __name__ == "__main__":
    main()
