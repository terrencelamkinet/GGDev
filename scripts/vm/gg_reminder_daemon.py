#!/usr/bin/env python3
"""
GG Reminder Scheduler Daemon v1
================================
Self-contained reminder system. Independent of gg_event_logger_v2.
Writes its own log files only.

Principle: 每個program都要寫log，但唔經中央log system。

Features:
  1. NLU parser — 「後日10點有會」「5分鐘後提我」「每月16號」
  2. State machine — pending → sent → confirmed/dismissed/overdue
  3. 30s scheduler loop — check due events, send reminders
  4. One-shot + recurring + relative time + birthday auto-check
  5. GG queryable — pending/overdue/status
  6. Confirm flow — send → user confirm → mark done
  7. Snooze / quiet hours / daily cap

Log Files (independent):
  ~/.openclaw/logs/gg-reminder/reminder-events.jsonl   — operation audit
  ~/.openclaw/logs/gg-reminder/reminder-health.log     — daemon health
  ~/.openclaw/logs/gg-reminder/reminder-state.json      — persistent state

References:
  - reed1898/reminder: NLU parsing + events.yml schema
  - focus-break-reminder: state machine pattern
  - martok9803/reminder-engine: cron lifecycle + relative time
  - manantra/birthday-reminder: recurring check + birthday logic
"""

import json
import os
import re
import sys
import time
import signal
import socket
import logging
import logging.handlers
import threading
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from typing import Optional, Any

# ════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════

BASE_DIR = Path("/home/airoot/.openclaw")
LOG_DIR = BASE_DIR / "logs" / "gg-reminder"
PID_FILE = BASE_DIR / "logs" / "gg-reminder.pid"

STATE_FILE = LOG_DIR / "reminder-state.json"
EVENTS_LOG = LOG_DIR / "reminder-events.jsonl"
HEALTH_LOG = LOG_DIR / "reminder-health.log"

TZ = timezone(timedelta(hours=8))

INTERVAL_S = 30           # main loop interval
QUIET_HOURS = (0, 6.5)    # 00:00 - 06:30 HKT, no reminders
DAILY_CAP = 8             # max reminders per day
COOLDOWN_MIN = 2          # min between reminders
CALENDAR_CHECK_INTERVAL = 300  # check Notion calendar every 5 min
KINETIX_ICS_URL = "https://outlook.office365.com/owa/calendar/23025923e672405cb1bcf881dcdd1e32@kinetix.com.hk/34fde7f166474af5ab31916b7fc8490c11023895445072650156/S-1-8-2393449578-217208843-2629041897-1723878112/reachcalendar.ics"

# ════════════════════════════════════════════════════════════════
# LOGGING — completely independent, writes its own files only
# ════════════════════════════════════════════════════════════════

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Health log (rotating)
    lgr = logging.getLogger("gg_reminder")
    lgr.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    fh = logging.handlers.RotatingFileHandler(HEALTH_LOG, maxBytes=512*1024, backupCount=2)
    fh.setFormatter(fmt)
    lgr.addHandler(fh)
    return lgr

log: logging.Logger = None  # set by main()

# ════════════════════════════════════════════════════════════════
# EVENT LOG — independent JSONL (NOT gg_event_logger_v2)
# ════════════════════════════════════════════════════════════════

_event_counter = 0
_last_calendar_check = 0  # timestamp of last Notion calendar check
_last_kinetix_check = 0  # timestamp of last Kinetix calendar check
_last_gcal_check = 0  # timestamp of last Google Calendar check

def log_event(level: str, category: str, message: str, **extra):
    """Write to reminder-events.jsonl only. No cross-talk with gg-v2 events.jsonl."""
    global _event_counter
    _event_counter += 1
    ts = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S%z")
    host = socket.gethostname()
    event = {
        "event_id": f"RMDR-{datetime.now(TZ).strftime('%Y%m%d')}-{_event_counter:04d}",
        "ts": ts,
        "host": host,
        "level": level,
        "category": category,
        "source": "gg_reminder",
        "message": message,
    }
    event.update(extra)
    try:
        with open(EVENTS_LOG, "a") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception as e:
        if log:
            if log:
                log.error(f"Failed to write event: {e}")

# ════════════════════════════════════════════════════════════════
# STATE — persistent JSON, survives restarts
# ════════════════════════════════════════════════════════════════

state_lock = threading.Lock()

def _load_state() -> dict:
    """Load full state from disk."""
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except (json.JSONDecodeError, OSError) as e:
        log_event("ERROR", "state", f"Failed to load state: {e}")
    return {"reminders": [], "config": {}, "stats": {"reminded_today": 0, "today_key": ""}}

def _save_state(state: dict):
    """Atomically save state."""
    tmp = STATE_FILE.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False))
        tmp.replace(STATE_FILE)
    except OSError as e:
        log_event("ERROR", "state", f"Failed to save state: {e}")

_state = _load_state()

def _ensure_today_reset():
    """Reset daily cap if date changed."""
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    if _state.get("stats", {}).get("today_key") != today:
        _state["stats"] = {"reminded_today": 0, "today_key": today}

# ════════════════════════════════════════════════════════════════
# REMINDER STATE MACHINE
# ════════════════════════════════════════════════════════════════
# States:
#   pending     → created, not yet due
#   sent        → delivered to user, awaiting confirm/dismiss
#   confirmed   → user said "got it"
#   dismissed   → user said "skip/dismiss"
#   overdue     → sent but no response within grace period (e.g. 30min)
#   cancelled   → user cancelled before due
# ════════════════════════════════════════════════════════════════

REMINDER_STATES = {"pending", "sent", "confirmed", "dismissed", "overdue", "cancelled"}
GRACE_MINUTES = 30  # sent → overdue after this

_next_id_counter = 1

def _next_id() -> str:
    global _next_id_counter
    today = datetime.now(TZ).strftime("%Y%m%d")
    existing = _state.get("reminders", [])
    count = sum(1 for r in existing if r["id"].startswith(today))
    # Use max of existing count or internal counter
    n = max(count, _next_id_counter) + 1
    _next_id_counter = n
    # Millisecond suffix prevents ID collisions after daemon restart
    ms = datetime.now(TZ).strftime("%f")[:3]
    return f"RMDR-{today}-{n:04d}-{ms}"

# ── Public API ──────────────────────────────────────────────────

def add_reminder(
    title: str,
    start_dt: datetime,
    notes: str = "",
    repeat: str = "one-off",
    reminders_minutes: list[int] | None = None,
    birthday: bool = False,
    metadata: dict | None = None,
) -> str:
    """
    Add a reminder to the state machine.
    Returns reminder ID.
    
    Args:
        title: Reminder text
        start_dt: When to fire (timezone-aware)
        notes: Optional context
        repeat: one-off | daily | weekly | monthly | yearly
        reminders_minutes: Offsets before start to pre-remind (e.g. [1440, 60, 10])
        birthday: If True, uses birthday logic (age calc)
        metadata: Optional dict with extra info (source, area, etc.)
    """
    rid = _next_id()
    
    # Compute actual fire times from offsets
    fire_times = [start_dt]
    if reminders_minutes:
        for offset in reminders_minutes:
            if offset > 0:
                fire_times.append(start_dt - timedelta(minutes=offset))
    
    # De-duplicate by sorting unique
    fire_times = sorted(set(fire_times))
    
    reminder = {
        "id": rid,
        "title": title,
        "notes": notes,
        "repeat": repeat,
        "birthday": birthday,
        "state": "pending",
        "fire_times": [ft.isoformat() for ft in fire_times],
        "next_fire": start_dt.isoformat(),
        "start_dt": start_dt.isoformat(),
        "created_at": datetime.now(TZ).isoformat(),
        "sent_at": None,
        "confirmed_at": None,
        "dismissed_at": None,
        "cancelled_at": None,
        "snooze_until": None,
        "delivery_count": 0,
        "metadata": metadata or {},
    }
    
    with state_lock:
        _state.setdefault("reminders", []).append(reminder)
        _save_state(_state)
    
    log_event("INFO", "create", f"Reminder created: {rid} — {title}", reminder_id=rid)
    if log:
        log.info(f"Created reminder {rid}: {title} @ {start_dt.strftime('%Y-%m-%d %H:%M')}")
    return rid


def add_birthday_reminder(name: str, day: int, month: int, year_born: int | None = None):
    """
    Add a birthday reminder that fires 7d, 1d, and on the day.
    Uses birthday-reminder logic: calculate turning age, check yearly.
    """
    now = datetime.now(TZ)
    bd_this_year = now.replace(month=month, day=day, hour=9, minute=0, second=0, microsecond=0)
    if bd_this_year < now:
        bd_this_year = bd_this_year.replace(year=now.year + 1)
    
    age = None
    if year_born:
        age = bd_this_year.year - year_born
    age_str = f" (turns {age})" if age else ""
    
    title = f"🎂 {name} birthday{age_str}!"
    
    # 7 days before + 1 day before
    reminders_minutes = [7 * 24 * 60, 24 * 60]
    
    rid = add_reminder(
        title=title,
        start_dt=bd_this_year,
        notes=f"{name}'s birthday — {day:02d}/{month:02d}" + (f" (born {year_born})" if year_born else ""),
        repeat="yearly",
        reminders_minutes=reminders_minutes,
        birthday=True,
    )
    return rid


def add_relative_reminder(title: str, minutes_from_now: int, notes: str = "") -> str:
    """Add a reminder relative to now (e.g. 'in 5 minutes')."""
    start_dt = datetime.now(TZ) + timedelta(minutes=minutes_from_now)
    return add_reminder(title=title, start_dt=start_dt, notes=notes)


def get_reminders(state_filter: str | None = None) -> list[dict]:
    """Get reminders, optionally filtered by state."""
    with state_lock:
        reminders = list(_state.get("reminders", []))
    
    if state_filter:
        if state_filter == "due":
            now = datetime.now(TZ)
            return [r for r in reminders
                    if r["state"] == "pending" and _parse_dt(r["next_fire"]) and _parse_dt(r["next_fire"]) <= now]
        return [r for r in reminders if r["state"] == state_filter]
    return reminders


def get_upcoming(days: int = 7) -> list[dict]:
    """Get all reminders due within N days."""
    now = datetime.now(TZ)
    cutoff = now + timedelta(days=days)
    upcoming = []
    for r in get_reminders():
        nf = _parse_dt(r.get("next_fire"))
        if nf and now <= nf <= cutoff and r["state"] in ("pending",):
            upcoming.append(r)
    return sorted(upcoming, key=lambda x: x["next_fire"])


def update_state(reminder_id: str, new_state: str) -> bool:
    """Transition a reminder to a new state. Returns True if successful."""
    if new_state not in REMINDER_STATES:
        log_event("WARN", "invalid", f"Invalid state transition: {new_state}", reminder_id=reminder_id)
        return False
    
    with state_lock:
        for r in _state.get("reminders", []):
            if r["id"] == reminder_id:
                if r["state"] == new_state:
                    return True  # idempotent
                old_state = r["state"]
                r["state"] = new_state
                now = datetime.now(TZ).isoformat()
                if new_state == "sent":
                    r["sent_at"] = now
                    r["delivery_count"] = r.get("delivery_count", 0) + 1
                elif new_state == "confirmed":
                    r["confirmed_at"] = now
                elif new_state == "dismissed":
                    r["dismissed_at"] = now
                elif new_state == "cancelled":
                    r["cancelled_at"] = now
                _save_state(_state)
                log_event("INFO", "transition", f"{reminder_id}: {old_state} → {new_state}",
                          reminder_id=reminder_id, old=old_state, new=new_state)
                if log:
                    log.info(f"State transition: {reminder_id} {old_state} → {new_state}")
                return True
    
    log_event("WARN", "not_found", f"Reminder not found: {reminder_id}")
    return False


def cancel_reminder(reminder_id: str) -> bool:
    """Cancel a pending reminder."""
    return update_state(reminder_id, "cancelled")


def snooze_reminder(reminder_id: str, minutes: int = 10) -> bool:
    """Snooze a reminder — set snooze_until, keep pending."""
    snooze_until = datetime.now(TZ) + timedelta(minutes=minutes)
    with state_lock:
        for r in _state.get("reminders", []):
            if r["id"] == reminder_id and r["state"] in ("sent", "pending"):
                r["snooze_until"] = snooze_until.isoformat()
                r["state"] = "pending"
                _save_state(_state)
                log_event("INFO", "snooze", f"{reminder_id} snoozed {minutes}min",
                          reminder_id=reminder_id, snooze_min=minutes)
                if log:
                    log.info(f"Snoozed {reminder_id} for {minutes}min")
                return True
    return False


def delete_reminder(reminder_id: str) -> bool:
    """Permanently remove a reminder."""
    with state_lock:
        before = len(_state.get("reminders", []))
        _state["reminders"] = [r for r in _state["reminders"] if r["id"] != reminder_id]
        after = len(_state["reminders"])
        if before != after:
            _save_state(_state)
            log_event("INFO", "delete", f"{reminder_id} deleted")
            if log:
                if log:
                    log.info(f"Deleted reminder {reminder_id}")
            return True
    return False


def get_stats() -> dict:
    """Get reminder daemon stats."""
    with state_lock:
        all_r = list(_state.get("reminders", []))
    
    counts = {"total": len(all_r), "pending": 0, "sent": 0, "confirmed": 0,
              "dismissed": 0, "overdue": 0, "cancelled": 0}
    for r in all_r:
        s = r.get("state", "pending")
        if s in counts:
            counts[s] += 1
    counts["today_sent"] = _state.get("stats", {}).get("reminded_today", 0)
    return counts


# ════════════════════════════════════════════════════════════════
# NLU PARSER — from reed1898/reminder + martok9803/reminder-engine
# ════════════════════════════════════════════════════════════════

PAT_TIME = re.compile(r"(\d{1,2})[:：](\d{2})")
PAT_HOUR = re.compile(r"(\d{1,2})[時點](\d{0,2})(半|分)?")
PAT_RELATIVE = re.compile(
    r"(\d+)\s*(分鐘|分鐘後|分鍾|分|min)\s*(後)?"
    r"|(\d+)\s*(小時|個鐘|鐘頭|hour|hr|h)\s*(後)?"
    r"|(\d+)\s*(日|天|day)\s*(後)?"
    r"|半[個]?[鐘時]"
)

CN_NUM = {"一":1,"二":2,"兩":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10,"零":0}

def _chinese_to_int(s: str) -> int:
    if not s:
        return 0
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s in CN_NUM:
        return CN_NUM[s]
    if "十" in s:
        parts = s.split("十")
        tens = _chinese_to_int(parts[0]) if parts[0] else 1
        ones = _chinese_to_int(parts[1]) if len(parts) > 1 and parts[1] else 0
        return tens * 10 + ones
    return 0

def _resolve_relative_day(text: str) -> int:
    if re.search(r"(?<!大後)(今|呢)[日天]", text):
        return 0
    if re.search(r"(聽|明)[日天早]", text):
        return 1
    if re.search(r"(後)[日天]", text) and "大後" not in text:
        return 2
    if "大後" in text:
        return 3
    return 0

def _resolve_time(text: str) -> tuple[int, int] | None:
    m = PAT_TIME.search(text)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = PAT_HOUR.search(text)
    if m:
        h = int(m.group(1))
        if m.group(2):
            m_val = int(m.group(2))
        elif m.group(3) == "半":
            m_val = 30
        else:
            m_val = 0
        if re.search(r"(下[午晝]|晏[晝]|晚[上間])", text):
            if h < 12:
                h += 12
        elif re.search(r"(凌[晨早])", text) and h < 6:
            pass
        elif h < 7 and m_val == 0:
            pass  # keep ambiguous
        return h, m_val
    return None

def _resolve_relative_time(text: str) -> int | None:
    """Returns minutes from now, or None."""
    m = PAT_RELATIVE.search(text)
    if not m:
        return None
    if "半" in text and ("鐘" in text or "小時" in text):
        return 30
    if m.group(1):
        return int(m.group(1))
    if m.group(4):
        return int(m.group(4)) * 60
    if m.group(7):
        return int(m.group(7)) * 24 * 60
    return None


def parse_natural(text: str) -> dict:
    """
    Parse natural language reminder text.
    
    Returns dict with keys:
      title, repeat, notes, is_birthday,
      relative_min, days_offset, month_offset, hour, minute, month, day
    """
    result = {
        "title": text, "repeat": "one-off", "notes": "",
        "is_birthday": False, "relative_min": None,
        "days_offset": 0, "month_offset": 0,
        "hour": None, "minute": None, "month": None, "day": None,
    }
    
    # Birthday pattern
    if re.search(r"(生日|birthday)", text, re.I):
        result["is_birthday"] = True
        m = re.search(r"(\w{2,})\s*(?:的|既)?生日", text)
        if m:
            result["title"] = f"🎂 {m.group(1)}'s birthday"
        dm = re.search(r"(\d{1,2})[月/](\d{1,2})[日號]?", text)
        if dm:
            result["month"] = int(dm.group(1))
            result["day"] = int(dm.group(2))
        return result
    
    # Relative time (priority)
    rel = _resolve_relative_time(text)
    if rel is not None:
        result["relative_min"] = rel
        cleaned = re.sub(
            r"\d+\s*(分鐘|小時|日|天)\s*(後)?\s*(提[我醒]?|叫[我]?|通知[我]?|remind\s*(me)?)?\s*",
            "", text, flags=re.I
        ).strip()
        if cleaned:
            result["title"] = cleaned
        return result
    
    # Days offset
    result["days_offset"] = _resolve_relative_day(text)
    
    # Check for "每月X號" / "每星期X" pattern — day-only, NOT month_offset
    day_only_m = re.search(r"每[月星期週禮拜](\d{1,2})[號日]?", text)
    _has_specific_date = False
    if day_only_m:
        result["day"] = int(day_only_m.group(1))
        if "月" in day_only_m.group(0):
            result["_day_only"] = True  # flag for resolve_parsed
    else:
        # Specific date with month — check BEFORE month_offset to avoid conflict
        dm = re.search(r"(\d{1,2})[月/](\d{1,2})[日號]?", text)
        _has_specific_date = dm is not None and 1 <= int(dm.group(1)) <= 12  # month must be 1-12
        if _has_specific_date:
            result["month"] = int(dm.group(1))
            result["day"] = int(dm.group(2))
    
    # Month offset (only if no specific date was given and no day-only)
    if not _has_specific_date and not result.get("_day_only"):
        if re.search(r"(下[個]?月)", text):
            result["month_offset"] = 1
        elif re.search(r"(上[個]?月)", text):
            result["month_offset"] = -1
    
    # Time
    time_val = _resolve_time(text)
    if time_val:
        result["hour"], result["minute"] = time_val
    
    # Recurring
    if re.search(r"(每[日天]|每天|every\s*day|daily)", text, re.I):
        result["repeat"] = "daily"
    elif re.search(r"(每[月]|每月|every\s*month|monthly)", text, re.I):
        result["repeat"] = "monthly"
    elif re.search(r"(每[個]?[星期週禮拜][一二三四五六日天]?|every\s*week|weekly)", text, re.I):
        result["repeat"] = "weekly"
    elif re.search(r"(每[年]|每年|every\s*year|yearly)", text, re.I):
        result["repeat"] = "yearly"
    
    # Clean title
    cleaned = re.sub(
        r"(今|聽|明|後|大後)(日|天|朝|晚).{0,10}?|"
        r"(上|下)午\s*|\d{1,2}[:：]\d{2}\s*|\d{1,2}[時點]\s*\d{0,2}(分|半)?\s*|"
        r"(提[我醒]?|叫[我]?|通知[我]?|remind\s*(me)?)|"
        r"每[日天月年]\s*|每[星期週禮拜][一二三四五六日天]?\s*|"
        r"半[個]?[鐘時]\s*(後)?(提[我醒]?|叫[我]?)?|"
        r"\d{1,2}[號日]\s*",
        "", text, flags=re.I
    ).strip()
    if cleaned and cleaned != text:
        result["title"] = cleaned
    
    return result


def resolve_parsed(parsed: dict) -> dict | None:
    """
    Resolve a parsed reminder into absolute datetime.
    Returns dict with start_dt, title, repeat, notes, reminders_minutes, is_birthday.
    """
    now = datetime.now(TZ)
    
    # Relative time
    if parsed.get("relative_min"):
        start = now + timedelta(minutes=parsed["relative_min"])
        return {"start_dt": start, "title": parsed["title"], "repeat": parsed["repeat"],
                "notes": "", "reminders_minutes": None, "is_birthday": False}
    
    # Birthday
    if parsed.get("is_birthday"):
        from calendar import monthrange
        month = parsed.get("month", now.month)
        day = parsed.get("day", now.day)
        max_day = monthrange(now.year, month)[1]
        if day > max_day:
            day = max_day
        bd = now.replace(month=month, day=day, hour=9, minute=0, second=0, microsecond=0)
        if bd <= now:
            bd = bd.replace(year=now.year + 1)
        return {"start_dt": bd, "title": parsed["title"], "repeat": "yearly",
                "notes": f"{parsed['title']} — {month:02d}/{day:02d}",
                "reminders_minutes": [7*24*60, 24*60], "is_birthday": True}
    
    from calendar import monthrange
    days = parsed.get("days_offset", 0)
    month_offset = parsed.get("month_offset", 0)
    target_date = now.date() + timedelta(days=days)
    
    # Handle "每月X號" — next occurrence of this day in future (this month or next)
    if parsed.get("_day_only"):
        day = parsed["day"]
        target_month = now.month
        target_year = now.year
        max_day = monthrange(target_year, target_month)[1]
        if day > max_day:
            day = max_day
        target_date = target_date.replace(day=day)
        # If already past this month, go to next month
        test_dt = datetime.combine(target_date, datetime.min.time().replace(hour=23, minute=59)).replace(tzinfo=TZ)
        if test_dt < now:
            target_month += 1
            if target_month > 12:
                target_month -= 12
                target_year += 1
            max_day = monthrange(target_year, target_month)[1]
            target_date = date(target_year, target_month, min(day, max_day))
        start_dt = datetime.combine(target_date, datetime.min.time().replace(hour=9, minute=0)).replace(tzinfo=TZ)
        return {"start_dt": start_dt, "title": parsed["title"], "repeat": "monthly",
                "notes": "", "reminders_minutes": None, "is_birthday": False}
    
    if month_offset and "month" not in parsed:
        target_month = now.month + month_offset
        target_year = now.year
        while target_month > 12:
            target_month -= 12
            target_year += 1
        while target_month < 1:
            target_month += 12
            target_year -= 1
        max_day = monthrange(target_year, target_month)[1]
        target_date = target_date.replace(year=target_year, month=target_month,
                                          day=min(target_date.day, max_day))
    
    if parsed.get("month") and parsed.get("day"):
        try:
            target_date = target_date.replace(month=parsed["month"], day=parsed["day"])
        except ValueError:
            return None
    
    hour = parsed.get("hour") or 9
    minute = parsed.get("minute") or 0
    start_dt = datetime.combine(target_date, datetime.min.time().replace(hour=hour, minute=minute)).replace(tzinfo=TZ)
    
    if start_dt < now:
        if parsed["repeat"] == "daily":
            while start_dt < now:
                start_dt += timedelta(days=1)
        elif parsed["repeat"] == "weekly":
            while start_dt < now:
                start_dt += timedelta(weeks=1)
        elif parsed["repeat"] == "monthly":
            while start_dt < now:
                nm = start_dt.month + 1
                ny = start_dt.year
                if nm > 12:
                    nm -= 12
                    ny += 1
                md = monthrange(ny, nm)[1]
                start_dt = start_dt.replace(year=ny, month=nm, day=min(start_dt.day, md))
        elif parsed["repeat"] == "yearly":
            start_dt = start_dt.replace(year=start_dt.year + 1)
        else:
            start_dt = start_dt.replace(year=now.year, month=now.month, day=now.day) + timedelta(days=1)
    
    return {"start_dt": start_dt, "title": parsed["title"], "repeat": parsed["repeat"],
            "notes": parsed.get("notes", ""), "reminders_minutes": None,
            "is_birthday": False}


# ════════════════════════════════════════════════════════════════
# NOTION CALENDAR CHECK
# ════════════════════════════════════════════════════════════════

def check_notion_calendar():
    """
    Query Notion Task Center for tasks due today or with Do Date = today.
    Create reminders in gg_reminder state for tasks not yet reminded.
    Runs at most once every 5 minutes.
    """
    import urllib.request
    
    logger = logging.getLogger('gg_reminder')
    
    key_path = os.path.expanduser('~/.config/notion/api_key')
    if not os.path.exists(key_path):
        logger.debug("Notion API key not found, skipping calendar check")
        return
    
    with open(key_path) as f:
        api_key = f.read().strip()
    
    data_source_id = '63161371-2aa4-460a-9758-c125709e1489'
    today = datetime.now(TZ).strftime('%Y-%m-%d')
    
    req = urllib.request.Request(
        f'https://api.notion.com/v1/data_sources/{data_source_id}/query',
        data=json.dumps({"page_size": 100}).encode(),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Notion-Version': '2025-09-03',
            'Content-Type': 'application/json'
        }
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.load(resp)
    except Exception as e:
        logger.error(f"Notion calendar query failed: {e}")
        log_event("ERROR", "notion", f"Calendar query failed: {e}")
        return
    
    results = data.get('results', [])
    now = datetime.now(TZ)
    
    with state_lock:
        existing = list(_state.get('reminders', []))
    existing_titles = {r['title'] for r in existing}
    
    added_count = 0
    for r in results:
        props = r.get('properties', {})
        
        # Skip completed/cancelled
        status = ''
        if 'Status' in props and props['Status'].get('status'):
            status = props['Status']['status'].get('name', '')
        if status in ('Done', 'Cancelled'):
            continue
        
        # Get title
        title = ''
        if 'Name' in props and props['Name'].get('title'):
            title = props['Name']['title'][0].get('plain_text', '')
        if not title:
            continue
        
        # Check Due Date and Do Date
        due_date = None
        if 'Due Date' in props and props['Due Date'].get('date'):
            due_date = props['Due Date']['date'].get('start', '')
        
        do_date = None
        if 'Do Date' in props and props['Do Date'].get('date'):
            do_date = props['Do Date']['date'].get('start', '')
        
        # Get area for metadata
        area = ''
        if 'Area' in props and props['Area'].get('select'):
            area = props['Area']['select'].get('name', '')
        
        is_today = (due_date == today) or (do_date == today)
        if not is_today:
            continue
        
        # Create a unique reminder title
        reminder_title = f"📋 {title}"
        
        if reminder_title in existing_titles:
            continue  # Already have this reminder
        
        # Calculate due time — end of day by default
        due_time = now.replace(hour=22, minute=0, second=0, microsecond=0)
        
        # Add as one-shot reminder
        add_reminder(
            reminder_title,
            due_time,
            notes=f"From Notion Task Center ({area})" if area else "From Notion Task Center",
            repeat="one-off",
            reminders_minutes=[60],  # 1 hour pre-remind for Notion tasks
            metadata={
                "source": "notion_calendar",
                "area": area,
                "status": status,
                "notion_title": title,
                "due_date": due_date or "",
                "do_date": do_date or "",
                "is_calendar_task": True
            }
        )
        
        existing_titles.add(reminder_title)
        added_count += 1
        logger.info(f"Calendar reminder added: {reminder_title}")
        log_event("INFO", "notion_calendar", f"Task added: {reminder_title} (area={area}, status={status})")
    
    if added_count > 0 or results:
        logger.info(f"Notion calendar check: {added_count} new, {len(results)} tasks scanned")
        log_event("INFO", "notion_calendar", f"Check complete: {added_count} new out of {len(results)} tasks")
    else:
        logger.debug(f"Notion calendar check: 0 new tasks for {today}")


# ════════════════════════════════════════════════════════════════
# KINETIX OUTLOOK 365 CALENDAR CHECK
# ════════════════════════════════════════════════════════════════

def check_kinetix_calendar():
    """
    Fetch Kinetix Outlook 365 ICS feed and create reminders for today's events.
    Runs at most once every 5 minutes.
    """
    import urllib.request
    import re as _re

    logger = logging.getLogger('gg_reminder')
    now = datetime.now(TZ)
    today_str = now.strftime('%Y%m%d')

    with state_lock:
        existing = list(_state.get('reminders', []))
    existing_titles = {r['title'] for r in existing}

    try:
        with urllib.request.urlopen(KINETIX_ICS_URL, timeout=10) as r:
            ics = r.read().decode('utf-8')
    except Exception as e:
        logger.error(f"Kinetix ICS fetch failed: {e}")
        log_event("ERROR", "kinetix", f"ICS fetch failed: {e}")
        return

    blocks = _re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', ics, _re.DOTALL)
    added = 0

    for block in blocks:
        # Extract date
        m = _re.search(r'DTSTART(?:;TZID[^:]*)?:(20\d{6})', block)
        if not m:
            continue
        date_str = m.group(1)

        # Only today's events
        if date_str != today_str:
            continue

        # Extract time
        time_match = _re.search(r'DTSTART(?:;TZID[^:]*)?:(20\d{6})T(\d{4})', block)
        event_time_str = time_match.group(2) if time_match else ''

        # Extract summary
        sm = _re.search(r'SUMMARY:(.*?)(?:\r?\n|$)', block)
        summary = sm.group(1).strip().replace(r'\,', ',') if sm else '(no title)'

        # Extract end time for duration
        end_match = _re.search(r'DTEND(?:;TZID[^:]*)?:(20\d{6})T(\d{4})', block)
        end_time_str = end_match.group(2) if end_match else ''

        # Create reminder title
        if event_time_str:
            hour = int(event_time_str[:2])
            minute = int(event_time_str[2:4])
            time_label = f"{hour:02d}:{minute:02d}"
            reminder_title = f"\N{TELEPHONE RECEIVER}[{time_label}] {summary}"

            # Set due time to event start
            due_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if due_time < now:
                # Event already started or passed
                continue
        else:
            reminder_title = f"\N{TELEPHONE RECEIVER} {summary}"
            due_time = now.replace(hour=23, minute=59, second=0, microsecond=0)

        # Skip if already exists
        if reminder_title in existing_titles:
            continue

        add_reminder(
            title=reminder_title,
            start_dt=due_time,
            notes=f"Kinetix Outlook 365 event",
            repeat="one-off",
            reminders_minutes=[60],  # 1 hour pre-remind for work events
            metadata={
                "source": "kinetix_ics",
                "original_title": summary,
                "time": event_time_str,
                "end_time": end_time_str
            }
        )
        existing_titles.add(reminder_title)
        added += 1
        logger.info(f"Kinetix reminder added: {reminder_title}")
        log_event("INFO", "kinetix", f"Event added: {reminder_title}")

    if added > 0:
        logger.info(f"Kinetix calendar: {added} event(s) added for today")
        log_event("INFO", "kinetix", f"Check complete: {added} new events")
    else:
        logger.debug("Kinetix calendar: 0 new events for today")


# ════════════════════════════════════════════════════════════════
# GOOGLE CALENDAR CHECK
# ════════════════════════════════════════════════════════════════

def check_google_calendar():
    """
    Fetch Google Calendar events for today and create reminders.
    Uses existing OAuth token at ~/.config/gcalcli/token.json.
    Runs at most once every 5 minutes.
    """
    logger = logging.getLogger('gg_reminder')
    now = datetime.now(TZ)
    today_str = now.strftime('%Y%m%d')
    
    with state_lock:
        existing = list(_state.get('reminders', []))
    existing_titles = {r['title'] for r in existing}
    
    token_file = os.path.expanduser('~/.config/gcalcli/token.json')
    if not os.path.exists(token_file):
        logger.debug("Google Calendar token not found, skipping")
        return
    
    try:
        with open(token_file) as f:
            tok = json.load(f)
        
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_authorized_user_info(tok)
        service = build('calendar', 'v3', credentials=creds)
        
        # Today's range in UTC
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
        day_end = now.replace(hour=23, minute=59, second=59, microsecond=0).astimezone(timezone.utc)
        
        events = service.events().list(
            calendarId='tunglamzt@gmail.com',
            timeMin=day_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            timeMax=day_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        added = 0
        for event in events.get('items', []):
            start_str = event['start'].get('dateTime', event['start'].get('date'))
            if 'T' not in start_str:
                continue  # skip all-day events
            
            summary = event['summary']
            
            try:
                if start_str.endswith('+08:00'):
                    event_dt = datetime.fromisoformat(start_str)
                elif start_str.endswith('Z'):
                    event_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                else:
                    logger.debug(f"Skipping event with unknown tz: {summary}")
                    continue
            except Exception:
                logger.debug(f"Cannot parse time for: {summary}")
                continue
            
            event_local = event_dt.astimezone(TZ)
            
            if event_local < now:
                continue  # skip past events
            
            time_label = event_local.strftime('%H:%M')
            reminder_title = f"\U0001F4C5 [{time_label}] {summary}"
            
            if reminder_title in existing_titles:
                continue
            
            location_text = event.get('location', '')
            description_text = event.get('description', '')

            add_reminder(
                reminder_title,
                event_local,
                repeat="once",
                reminders_minutes=[60],  # 1 hour pre-remind
                metadata={
                    "source": "google_calendar",
                    "original_title": summary,
                    "calendar": "tunglamzt@gmail.com",
                    "location": location_text,
                    "description": description_text
                }
            )
            existing_titles.add(reminder_title)
            added += 1
            logger.info(f"Google Calendar reminder added: {reminder_title}")
        
        if added > 0:
            logger.info(f"Google Calendar: {added} event(s) added for today")
            log_event("INFO", "gcal", f"{added} event(s) added for today")
        else:
            logger.debug("Google Calendar: no new events for today")
    
    except Exception as e:
        logger.error(f"Google Calendar check failed: {e}")
        log_event("ERROR", "gcal", f"Check failed: {e}")


# ════════════════════════════════════════════════════════════════
# SCHEDULER — main loop
# ════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════
# TELEGRAM DELIVERY — push notifications to Terrence
# ════════════════════════════════════════════════════════════════

TELEGRAM_BOT_TOKEN = "8682669253:AAEjCwU5LmDZhxeejwVOFdFp3Xm5_PMHfug"
TELEGRAM_CHAT_ID = "7380833889"
DELIVERY_QUEUE_FILE = LOG_DIR / "pending_deliveries.jsonl"


def deliver_reminder(reminder: dict):
    """
    Send reminder to Terrence's Telegram immediately.
    Falls back to delivery queue file if HTTP send fails.
    
    For calendar-sourced reminders (google_calendar, kinetix_ics),
    uses the smart context engine to build a rich message with
    Notion task merge, location, and navigation info.
    """
    logger = logging.getLogger('gg_reminder')
    
    title = reminder["title"]
    notes = reminder.get("notes", "")
    rid = reminder["id"]
    meta = reminder.get("metadata", {})
    source = meta.get("source", "")
    
    # Use smart context for calendar-sourced reminders
    if source in ("google_calendar", "kinetix_ics"):
        try:
            from gg_reminder_context import build_smart_reminder
            
            # Strip emoji prefix for clean title
            clean_title = re.sub(r'^[\U0001F4C5\U0001F4E0]\s*\[?[\d:]{4,5}\]?\s*', '', title).strip()
            
            event_time = reminder.get("start_dt", "")
            location = meta.get("location", "")
            description = meta.get("description", "")
            
            # Kinetix ICS = always Kwun Tong office
            if source == "kinetix_ics" and not location:
                location = "Kinetix"
            
            message = build_smart_reminder(
                event_title=clean_title,
                event_time_str=event_time,
                location_text=location,
                description=description
            )
        except Exception as e:
            logger.warning(f"Smart context failed, using basic: {e}")
            message = f"⏰ *{title}*"
            if notes:
                message += f"\n\n{notes}"
    else:
        # Basic reminder for non-calendar sources
        message = f"⏰ *{title}*"
        if notes:
            message += f"\n\n{notes}"
    
    # Try direct Telegram API send
    success = _send_telegram(message)
    
    if success:
        logger.info(f"Delivered: {rid} — {title}")
        log_event("INFO", "deliver", f"Delivered: {rid} — {title}", reminder_id=rid)
        return
    
    # Fallback: queue to file
    _enqueue_delivery(reminder)


def _send_telegram(text: str) -> bool:
    """Send a message to Terrence's Telegram. Returns True on success."""
    import urllib.request
    
    api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    body = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_notification": False,
    }).encode()
    
    try:
        req = urllib.request.Request(api, data=body,
                                     headers={"Content-Type": "application/json"},
                                     method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception:
        return False


def _enqueue_delivery(reminder: dict):
    """Write reminder to delivery queue file for later pickup."""
    logger = logging.getLogger('gg_reminder')
    
    delivery = {
        "title": reminder["title"],
        "notes": reminder.get("notes", ""),
        "id": reminder["id"],
        "source": reminder.get("metadata", {}).get("source", "reminder"),
        "original_title": reminder.get("metadata", {}).get("original_title", ""),
        "created_at": datetime.now(TZ).isoformat()
    }
    
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(DELIVERY_QUEUE_FILE, "a") as f:
            f.write(json.dumps(delivery, ensure_ascii=False) + "\n")
        logger.info(f"Enqueued delivery: {reminder['title']}")
    except Exception as e:
        logger.error(f"Failed to enqueue delivery: {e}")


def flush_delivery_queue():
    """
    Retry sending any queued deliveries that didn't go through.
    Called periodically in the main loop.
    """
    logger = logging.getLogger('gg_reminder')
    
    if not DELIVERY_QUEUE_FILE.exists():
        return
    
    try:
        with open(DELIVERY_QUEUE_FILE, "r") as f:
            lines = f.readlines()
        
        if not lines:
            return
        
        remaining = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                delivery = json.loads(line)
                title = delivery.get("title", "Reminder")
                notes = delivery.get("notes", "")
                msg = f"\u23f0 *{title}*"
                if notes:
                    msg += f"\n\n{notes}"
                
                if not _send_telegram(msg):
                    remaining.append(line)
            except (json.JSONDecodeError, KeyError):
                remaining.append(line)
        
        # Write back remaining (failed) or clear if all succeeded
        if remaining:
            with open(DELIVERY_QUEUE_FILE, "w") as f:
                f.writelines(remaining)
            logger.info(f"Delivery queue: {len(lines)} attempted, {len(remaining)} remaining")
        else:
            # Clear the file
            open(DELIVERY_QUEUE_FILE, "w").close()
            logger.info(f"Delivery queue: {len(lines)} all delivered, queue cleared")
    except Exception as e:
        logger.error(f"Failed to flush delivery queue: {e}")


# ════════════════════════════════════════════════════════════════


def _parse_dt(iso_str: str | None) -> datetime | None:
    if not iso_str:
        return None
    try:
        return datetime.fromisoformat(iso_str)
    except (ValueError, TypeError):
        return None


def compute_next_fire(reminder: dict) -> str | None:
    """Compute next fire time for recurring reminders."""
    if reminder.get("repeat", "one-off") == "one-off":
        return None
    
    now = datetime.now(TZ)
    start = _parse_dt(reminder["start_dt"])
    if not start:
        return None
    
    next_dt = None
    repeat = reminder["repeat"]
    
    if repeat == "daily":
        next_dt = start + timedelta(days=(now - start).days + 1)
    elif repeat == "weekly":
        next_dt = start + timedelta(weeks=((now - start).days // 7) + 1)
    elif repeat == "monthly":
        from calendar import monthrange
        next_dt = start
        while next_dt <= now:
            nm = next_dt.month + 1
            ny = next_dt.year
            if nm > 12:
                nm -= 12
                ny += 1
            md = monthrange(ny, nm)[1]
            next_dt = next_dt.replace(year=ny, month=nm, day=min(next_dt.day, md))
    elif repeat == "yearly":
        next_dt = start.replace(year=now.year + 1)
    
    return next_dt.isoformat() if next_dt else None


def _is_quiet_hours() -> bool:
    now = datetime.now(TZ)
    hour = now.hour + now.minute / 60
    start, end = QUIET_HOURS
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


def process_due_reminders() -> list[dict]:
    """
    Check all reminders and send ones that are due.
    Called every loop iteration. Returns list of sent reminders.
    The actual send is delegated to the calling loop (this just transitions state).
    """
    now = datetime.now(TZ)
    due = []
    
    with state_lock:
        _ensure_today_reset()
        if _state["stats"]["reminded_today"] >= DAILY_CAP:
            return due
        reminders = list(_state.get("reminders", []))
    
    if _is_quiet_hours():
        return due
    
    for r in reminders:
        if r["state"] not in ("pending", "sent"):
            continue
        
        snooze_until = _parse_dt(r.get("snooze_until"))
        if snooze_until and snooze_until > now:
            continue
        
        # Multi-fire: check if ANY fire_time is due or past
        fire_times = r.get("fire_times", [])
        sent_times = set(r.get("_sent_fire_times", []))
        unsent_fire = None
        
        for ft_str in fire_times:
            ft = _parse_dt(ft_str)
            if ft and ft <= now and ft_str not in sent_times:
                unsent_fire = ft
                break
        
        next_fire = _parse_dt(r.get("next_fire"))
        
        if unsent_fire:
            # Found an unsent fire time that's due → use it for delivery
            next_fire = unsent_fire
        elif not next_fire or next_fire > now:
            continue
        
        if r["state"] == "sent":
            sent_at = _parse_dt(r.get("sent_at"))
            if sent_at and (now - sent_at).total_seconds() > GRACE_MINUTES * 60:
                update_state(r["id"], "overdue")
            continue
        
        # Record which fire_time was sent
        if unsent_fire:
            with state_lock:
                sent_times = set(r.get("_sent_fire_times", []))
                sent_times.add(unsent_fire.isoformat())
                r["_sent_fire_times"] = list(sent_times)
                _save_state(_state)
        
        # Mark sent
        with state_lock:
            _state["stats"]["reminded_today"] += 1
        update_state(r["id"], "sent")
        
        # Deliver via Telegram
        r_copy = dict(r)  # copy because we have state_lock
        deliver_reminder(r_copy)
        
        due.append(r)
        log_event("INFO", "send", f"Reminder due: {r['id']} — {r['title']}",
                  reminder_id=r["id"])
        if log:
            log.info(f"Due: {r['id']} — {r['title']}")
    
    return due


def schedule_next_occurrence(reminder_id: str):
    """For recurring reminders, compute and set next fire time."""
    with state_lock:
        for r in _state.get("reminders", []):
            if r["id"] != reminder_id:
                continue
            if r.get("repeat", "one-off") == "one-off":
                continue
            next_fire = compute_next_fire(r)
            if next_fire:
                r["state"] = "pending"
                r["next_fire"] = next_fire
                _save_state(_state)
                log_event("INFO", "reschedule", f"{reminder_id} → {next_fire}",
                          reminder_id=reminder_id)
                if log:
                    log.info(f"Rescheduled {reminder_id} → {next_fire}")
            return


# ════════════════════════════════════════════════════════════════
# DAEMON LIFECYCLE
# ════════════════════════════════════════════════════════════════

_running = True

def signal_handler(signum, frame):
    global _running
    log.info(f"Received signal {signum}, shutting down...")
    log_event("INFO", "shutdown", f"Daemon shutting down (signal {signum})")
    _running = False


def main():
    global log
    log = setup_logging()
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    log.info("═══ GG Reminder Daemon v1 starting ═══")
    log_event("INFO", "startup", "Daemon started")
    
    # Write PID file
    try:
        PID_FILE.write_text(str(os.getpid()))
    except OSError as e:
        log.warning(f"Cannot write PID file: {e}")
    
    # Clean stale lock
    with state_lock:
        for r in _state.get("reminders", []):
            if r["state"] == "sent":
                # If daemon restarted while reminders were sent, re-mark as pending
                # to pick up overdue tracking
                pass
    
    cycle = 0
    while _running:
        cycle += 1
        loop_start = time.time()
        
        try:
            # Process due reminders (state transitions)
            due = process_due_reminders()
            
            # Calendar check every 5 min (not every 30s)
            global _last_calendar_check, _last_kinetix_check, _last_gcal_check
            if time.time() - _last_calendar_check > CALENDAR_CHECK_INTERVAL:
                check_notion_calendar()
                _last_calendar_check = time.time()

            # Kinetix Outlook 365 calendar check every 5 min
            if time.time() - _last_kinetix_check > 300:
                check_kinetix_calendar()
                _last_kinetix_check = time.time()

            # Google Calendar check every 5 min
            if time.time() - _last_gcal_check > 300:
                check_google_calendar()
                _last_gcal_check = time.time()

            # Log heartbeat every 20 cycles (10 min)
            # Flush delivery queue every 10 cycles (5 min)
            if cycle % 10 == 0:
                flush_delivery_queue()

            if cycle % 20 == 0:
                stats = get_stats()
                log.info(f"Heartbeat — total: {stats['total']}, pending: {stats['pending']}, "
                         f"today sent: {stats['today_sent']}")
                log_event("HEARTBEAT", "heartbeat", f"OK — {json.dumps(stats)}")
            
        except Exception as e:
            log.error(f"Cycle error: {e}", exc_info=True)
            log_event("ERROR", "cycle", f"Cycle {cycle} error: {e}")
        
        elapsed = time.time() - loop_start
        sleep_ms = max(1, INTERVAL_S - int(elapsed))
        time.sleep(sleep_ms)
    
    log.info("═══ GG Reminder Daemon stopped ═══")
    log_event("INFO", "shutdown", "Daemon stopped gracefully")


if __name__ == "__main__":
    main()
