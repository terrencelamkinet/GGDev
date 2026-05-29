#!/usr/bin/env python3
"""
Contracts Check Module — import into gg_reminder_daemon.py

Provides:
  - check_contracts(): Poll Notion Contracts DB every 5 min
  - _auto_update_remind_dates(): Weekly remind date maintenance

Design: Terrence Lam 2026-05-25
"""

import json
import os
import re
import logging
import urllib.request
from datetime import datetime, timezone, timedelta, date

# ════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════

CONTRACTS_DB = "29d783d5-93e7-8056-93fb-cd6756c2acc2"
API_KEY_PATH = os.path.expanduser("~/.config/notion/api_key")
NOTION_VERSION = "2022-06-28"

TZ = timezone(timedelta(hours=8))

# Payment term to relativedelta mapping
TERM_MAP = {
    "Yearly": {"years": 1},
    "Quarterly": {"months": 3},
    "Monthly": {"months": 1},
    "2 Years": {"years": 2},
    "5 Years": {"years": 5},
    "10 Years": {"years": 10},
    "3 Months": {"months": 3},
}

# Contracts that need remind dates (by Type)
REMINDABLE_TYPES = {"License", "Insurance", "Service", "Couse"}

# Contracts that are fixed monthly expenses (no remind needed)
FIXED_TYPES = {"Normal", "Loan"}

# Monthly insurance that's ongoing payment, not fixed-term renewal
MONTHLY_INSURANCE_TITLES = {
    "Terrence\u2019s AIA insurance", "Terrence\u2019s AIA insurance ",
    "Terrence's AIA insurance", "Terrence's AIA insurance ",
}

# Monthly-service contracts that don't need renewal reminders (monthly fees)
MONTHLY_SERVICE_TITLES = {
    "\u8eca\u4f4d\u79df\u91d1", "\u5165\u6cb9", "\u6cca\u8eca",
    "Terrence\u2019s \u4e2d\u570b\u79fb\u52d5 mobile", "Terrence\u2019s \u4e2d\u570b\u79fb\u52d5 mobile ",
    "Terrence's \u4e2d\u570b\u79fb\u52d5 mobile", "Terrence's \u4e2d\u570b\u79fb\u52d5 mobile ",
    "Apple family", "Apple family ",
}

# Already expired / handled — don't auto-set
SKIP_TITLES = {
    "HKBN Boardband",
    "\u6e2f\u8eca\u5317\u4e0a License",
}

# Services where monthly subscription is ongoing (not fixed-term renewal)
MONTHLY_SUBSCRIPTIONS = {"\u8eca\u4f4d\u79df\u91d1", "\u5165\u6cb9", "\u6cca\u8eca", "Apple family",
                         "Terrence\u2019s \u4e2d\u570b\u79fb\u52d5 mobile", "Terrence\u2019s \u4e2d\u570b\u79fb\u52d5 mobile ",
                         "Terrence's \u4e2d\u570b\u79fb\u52d5 mobile", "Terrence's \u4e2d\u570b\u79fb\u52d5 mobile "}

# Weekly auto-update interval (7 days in seconds)
WEEKLY_INTERVAL = 7 * 24 * 3600

# ════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════

def _normalize_name(name):
    """Normalize contract name: strip spaces, normalize U+2019 apostrophe to ASCII."""
    if not name:
        return ""
    return name.strip().replace("\u2019", "'")


def _get_notion_headers():
    """Return Notion API headers."""
    if not os.path.exists(API_KEY_PATH):
        return None
    with open(API_KEY_PATH) as f:
        api_key = f.read().strip()
    return {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _get_prop(page, field):
    """Safely extract a Notion property value."""
    props = page.get("properties", {})
    p = props.get(field, {})
    t = p.get("type", "")
    v = p.get(t)
    if v is None:
        return None
    if t == "title":
        return v[0].get("plain_text", "") if v else ""
    if t == "rich_text":
        return v[0].get("plain_text", "") if v else ""
    if t == "select":
        return v.get("name") if isinstance(v, dict) else None
    if t == "date":
        if isinstance(v, dict):
            return {"start": v.get("start"), "end": v.get("end")}
        return None
    if t == "number":
        return v
    return None


def _add_months(source_date, months):
    """Add months to a date, handling month-end overflow."""
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                                 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return date(year, month, day)


def _compute_remind_date(ctype, pay_term, start_str, end_str):
    """
    Compute remind date (30 days before due/renewal).
    
    Returns ISO date string or None if can't compute.
    """
    today = date.today()
    
    # If end date is explicit, use it
    if end_str:
        try:
            end_dt = date.fromisoformat(end_str.split("T")[0])
            remind = end_dt - timedelta(days=30)
            return remind.isoformat()
        except (ValueError, TypeError):
            pass
    
    # No end date, try to estimate from start + term
    if not start_str or not pay_term:
        return None
    
    try:
        start_dt = date.fromisoformat(start_str.split("T")[0])
    except (ValueError, TypeError):
        return None
    
    term_config = TERM_MAP.get(pay_term)
    if not term_config:
        return None
    
    # Calculate end = start + term
    years = term_config.get("years", 0)
    months = term_config.get("months", 0)
    
    if years:
        end_dt = start_dt.replace(year=start_dt.year + years)
    elif months:
        end_dt = _add_months(start_dt, months)
    else:
        return None
    
    # For multi-term contracts (passport 10yr, driver license 10yr):
    # Push end date forward until it's AFTER today (accounting for renewals)
    term_seconds = (years * 365 + months * 30) * 86400 if (years or months) else 0
    
    if end_dt <= today and term_seconds > 0:
        delta = timedelta(seconds=term_seconds)
        while end_dt <= today:
            end_dt = end_dt.__class__.fromordinal(end_dt.toordinal()) + delta
    
    remind = end_dt - timedelta(days=30)
    return remind.isoformat()


def _update_notion_page(page_id, remind_date_iso):
    """Update the Remind date field on a Notion page."""
    headers = _get_notion_headers()
    if not headers:
        return False
    
    url = f"https://api.notion.com/v1/pages/{page_id}"
    body = {
        "properties": {
            "Remind date": {
                "date": {"start": remind_date_iso}
            }
        }
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode(),
            headers=headers,
            method="PATCH"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("object") == "page"
    except Exception as e:
        logger = logging.getLogger("gg_reminder")
        logger.error(f"Failed to update remind date for {page_id}: {e}")
        return False


def _format_contract_reminder(contract):
    """Format a contract reminder message with inline buttons."""
    name = contract.get("title", "?")
    ctype = contract.get("type", "")
    cost = contract.get("cost", 0)
    pay_term = contract.get("pay_term", "")
    remind_date = contract.get("remind_date", "")
    detail = contract.get("detail", "")
    note = contract.get("note", "")
    start = contract.get("start_date", "")
    end = contract.get("end_date", "")
    
    # Build message
    lines = [f"💳 *{name}*"]
    
    if ctype:
        cost_str = ""
        if cost and pay_term:
            cost_str = f"  ${cost:,.2f}/{pay_term}"
        elif cost:
            cost_str = f"  ${cost:,.2f}"
        lines.append(f"   {ctype}{cost_str}")
    
    if remind_date:
        lines.append(f"   ⏰ Remind: {remind_date}")
    
    if start:
        lines.append(f"   📅 Start: {start[:10]}")
    if end:
        lines.append(f"   🔚 End: {end[:10]}")
    
    if detail:
        lines.append(f"   📝 {detail[:100]}")
    if note:
        lines.append(f"   📌 {note[:100]}")
    
    lines.append("")
    lines.append("你需要做啲咩？")
    
    return "\n".join(lines)


def _build_contract_keyboard(page_id, contract_name):
    """Build inline keyboard for contract reminder."""
    # Escape page_id for callback_data (Telegram has 64-byte limit)
    safe_id = page_id.replace("-", "")
    return [
        [
            {"text": "🔔 睇過", "callback_data": f"cntr:{safe_id}:seen"},
            {"text": "✅ 續約", "callback_data": f"cntr:{safe_id}:renew"},
        ],
        [
            {"text": "❌ 取消", "callback_data": f"cntr:{safe_id}:cancel"},
            {"text": "📝 Update", "callback_data": f"cntr:{safe_id}:update"},
        ],
    ]


# ════════════════════════════════════════════════════════════
# MAIN FUNCTIONS
# ════════════════════════════════════════════════════════════

# Lazy import from parent module
_send_telegram = None
_state_lock = None
_state = None
_log_event = None

def _import_globals():
    """Import shared state from gg_reminder_daemon module."""
    global _send_telegram, _state_lock, _state, _log_event
    import sys
    parent = sys.modules.get("__main__")
    if parent:
        _send_telegram = getattr(parent, "_send_telegram", None)
        _state_lock = getattr(parent, "state_lock", None)
        _state = getattr(parent, "_state", None)
        _log_event = getattr(parent, "log_event", None)


def check_contracts():
    """
    Poll Contracts DB for upcoming remind dates.
    
    - Runs every 5 minutes (called from daemon main loop)
    - Filters: Remind date <= today+7
    - Sends Telegram notification with inline buttons
    - Tracks which contracts have been notified in state
    
    Also auto-updates remind dates weekly:
    - For contracts with start+term but no remind date set
    - For contracts with stale remind dates (past due with no action)
    """
    logger = logging.getLogger("gg_reminder")
    
    # Import shared state
    _import_globals()
    if not _send_telegram:
        logger.warning("Cannot send Telegram: _send_telegram not available")
        return
    
    headers = _get_notion_headers()
    if not headers:
        logger.debug("Notion API key not found, skipping contracts check")
        return
    
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    next_week = (datetime.now(TZ) + timedelta(days=7)).strftime("%Y-%m-%d")
    
    # ── Query Contracts DB ──
    filter_body = {
        "filter": {
            "and": [
                {
                    "property": "Remind date",
                    "date": {
                        "on_or_before": next_week
                    }
                }
            ]
        },
        "page_size": 100,
        "sorts": [{"property": "Remind date", "direction": "ascending"}]
    }
    
    try:
        req = urllib.request.Request(
            f"https://api.notion.com/v1/databases/{CONTRACTS_DB}/query",
            data=json.dumps(filter_body).encode(),
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        logger.error(f"Contracts DB query failed: {e}")
        if _log_event:
            _log_event("ERROR", "contracts", f"Query failed: {e}")
        return
    
    results = data.get("results", [])
    if not results:
        logger.debug("Contracts check: no upcoming reminders")
        return
    
    # ── Check state machine ──
    if _state_lock:
        with _state_lock:
            notified = _state.get("contracts_notified", {})
    else:
        notified = {}
    
    now_ts = datetime.now(TZ).isoformat()
    sent_count = 0
    
    for page in results:
        page_id = page["id"]
        name = _get_prop(page, "Items") or "?"
        ctype = _get_prop(page, "Type") or ""
        cost = _get_prop(page, "Cost") or 0
        pay_term = _get_prop(page, "Payment Term") or ""
        rd = _get_prop(page, "Remind date")
        start = _get_prop(page, "Start Date")
        detail = _get_prop(page, "Detail") or ""
        remark = _get_prop(page, "Special Remark") or ""
        
        remind_date_str = rd["start"] if rd else None
        start_str = start["start"] if start else None
        end_str = start["end"] if start else None
        
        if not remind_date_str:
            continue
        
        # ── Skip quiet hours ──
        try:
            from gg_reminder_context import _is_quiet_hours
            if _is_quiet_hours():
                logger.debug("Quiet hours, deferring contract reminders")
                return
        except ImportError:
            pass
        
        # ── Check if already notified ──
        last_notified = notified.get(name)
        if last_notified:
            last_dt = datetime.fromisoformat(last_notified)
            now_dt = datetime.now(TZ)
            days_since = (now_dt - last_dt).days
            if days_since < 1 and remind_date_str <= today:
                # Already notified today for a due reminder
                continue
            elif days_since < 7:
                # Already notified this week
                continue
        
        # ── Determine urgency ──
        try:
            rd_dt = date.fromisoformat(remind_date_str)
            today_dt = date.today()
            days_until = (rd_dt - today_dt).days
        except (ValueError, TypeError):
            days_until = 999
        
        if days_until < 0:
            urgency_label = "🔴 OVERDUE"
        elif days_until == 0:
            urgency_label = "🔴 TODAY"
        elif days_until <= 3:
            urgency_label = "🟡 SOON"
        elif days_until <= 7:
            urgency_label = "🟢 UPCOMING"
        else:
            # Outside 7-day window, shouldn't reach here
            continue
        
        # ── Build contract info dict ──
        contract = {
            "title": name,
            "type": ctype,
            "cost": cost,
            "pay_term": pay_term,
            "remind_date": remind_date_str,
            "start_date": start_str,
            "end_date": end_str,
            "detail": detail,
            "note": remark,
        }
        
        # ── Send notification ──
        message = _format_contract_reminder(contract)
        
        # Add urgency header
        header_line = f"{urgency_label} 合約到期提醒"
        message = f"{header_line}\n{'-'*20}\n{message}"
        
        keyboard = _build_contract_keyboard(page_id, name)
        
        success = _send_telegram(message, keyboard=keyboard)
        
        if success:
            sent_count += 1
            # Update notified state
            if _state_lock:
                with _state_lock:
                    if "contracts_notified" not in _state:
                        _state["contracts_notified"] = {}
                    _state["contracts_notified"][name] = now_ts
            
            logger.info(f"Contracts reminder sent: {name} ({urgency_label})")
            if _log_event:
                _log_event("INFO", "contracts", 
                          f"Sent: {name} — remind={remind_date_str} ({urgency_label})")
    
    if sent_count > 0:
        logger.info(f"Contracts check: {sent_count} reminders sent out of {len(results)} upcoming")
        if _log_event:
            _log_event("INFO", "contracts", 
                      f"Check complete: {sent_count} sent / {len(results)} scanned")


def auto_update_remind_dates():
    """
    Weekly maintenance: scan all contracts and auto-compute remind dates.
    
    Rules:
    - License: remind 30 days before renewal (passports, driver license, etc.)
    - Insurance: remind 30 days before renewal
    - Service: remind 30 days before renewal if yearly/term-based
    - Loan: only if end date is known
    - Normal: skip (fixed monthly expenses)
    - Couse: remind 30 days before next payment if term known
    
    Only updates if:
      1. No remind date currently set
      2. Remind date has passed AND no action taken (overdue)
    """
    logger = logging.getLogger("gg_reminder")
    
    headers = _get_notion_headers()
    if not headers:
        logger.debug("Notion API key not found, skipping auto-update")
        return
    
    # ── Fetch all contracts ──
    try:
        req = urllib.request.Request(
            f"https://api.notion.com/v1/databases/{CONTRACTS_DB}/query",
            data=json.dumps({"page_size": 100}).encode(),
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        logger.error(f"Contracts auto-update fetch failed: {e}")
        return
    
    results = data.get("results", [])
    today_dt = date.today()
    
    updated = 0
    skipped = 0
    errors = 0
    
    for page in results:
        page_id = page["id"]
        name = _get_prop(page, "Items") or "?"
        ctype = _get_prop(page, "Type") or ""
        cost = _get_prop(page, "Cost") or 0
        pay_term = _get_prop(page, "Payment Term") or ""
        rd = _get_prop(page, "Remind date")
        start = _get_prop(page, "Start Date")
        remark = _get_prop(page, "Special Remark") or ""
        
        remind_date_str = rd["start"] if rd else None
        start_str = start["start"] if start else None
        end_str = start["end"] if start else None
        
        # Always skip Fixed / Loan types
        if ctype in FIXED_TYPES:
            skipped += 1
            continue
        
        # Skip monthly subscriptions
        if _normalize_name(name) in MONTHLY_SERVICE_TITLES or _normalize_name(name) in MONTHLY_SUBSCRIPTIONS:
            skipped += 1
            continue
        
        # Skip monthly insurance (ongoing, not fixed-term)
        if _normalize_name(name) in MONTHLY_INSURANCE_TITLES:
            skipped += 1
            continue
        
        # Skip known handled/expired
        if _normalize_name(name) in SKIP_TITLES:
            skipped += 1
            continue
        
        # ── Skip if not a remindable type ──
        if ctype not in REMINDABLE_TYPES:
            skipped += 1
            continue
        
        # ── Check: should we compute a remind date? ──
        if remind_date_str:
            try:
                rd_dt = date.fromisoformat(remind_date_str)
            except (ValueError, TypeError):
                rd_dt = None
            
            if rd_dt and rd_dt >= today_dt:
                # Current remind date is in the future, keep it
                skipped += 1
                continue
            
            # Current remind date passed - check if action was taken
            if rd_dt and rd_dt < today_dt:
                # If remark mentions "已續約" or "✅處理", skip
                if "已續約" in remark or "✅" in remark or "已處理" in remark:
                    # Still recompute for the next cycle
                    new_rd = _compute_remind_date(ctype, pay_term, start_str, end_str)
                    if new_rd and new_rd != remind_date_str:
                        if _update_notion_page(page_id, new_rd):
                            updated += 1
                            logger.info(f"Auto-updated remind date: {name} → {new_rd} (was {remind_date_str})")
                    continue
        
        # ── Compute new remind date ──
        new_rd = _compute_remind_date(ctype, pay_term, start_str, end_str)
        
        if not new_rd:
            logger.debug(f"Cannot compute remind date for {name}: missing start/term data")
            skipped += 1
            continue
        
        # ── Update Notion ──
        if _update_notion_page(page_id, new_rd):
            updated += 1
            logger.info(f"Set remind date: {name} → {new_rd}")
        else:
            errors += 1
            logger.error(f"Failed to update remind date for {name}")
    
    if updated > 0 or errors > 0:
        logger.info(f"Contracts auto-update: {updated} updated, {errors} errors, {skipped} skipped")
        if _log_event:
            _log_event("INFO", "contracts", 
                      f"Weekly update: {updated} updated, {errors} errors, {skipped} skipped")


# ════════════════════════════════════════════════════════════
# STANDALONE TEST
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=== Contracts Module Test ===")
    print(f"Today: {datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S HKT')}")
    print()
    
    print("=== Preview: computed remind dates for all contracts ===")
    
    headers = _get_notion_headers()
    if not headers:
        print("❌ Cannot access Notion API key")
        sys.exit(1)
    
    req = urllib.request.Request(
        f"https://api.notion.com/v1/databases/{CONTRACTS_DB}/query",
        data=json.dumps({"page_size": 100}).encode(),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    
    results = data.get("results", [])
    print(f"Total contracts: {len(results)}")
    print()
    
    need_update = []
    ok = []
    skip_list = []
    
    for page in results:
        page_id = page["id"]
        name = _get_prop(page, "Items") or "?"
        ctype = _get_prop(page, "Type") or ""
        cost = _get_prop(page, "Cost") or 0
        pay_term = _get_prop(page, "Payment Term") or ""
        rd = _get_prop(page, "Remind date")
        start = _get_prop(page, "Start Date")
        remind_date_str = rd["start"] if rd else None
        start_str = start["start"] if start else None
        end_str = start["end"] if start else None
        
        # Same filters as auto_update_remind_dates()
        if ctype in FIXED_TYPES:
            skip_list.append((name, "固定支出/分期"))
            continue
        if _normalize_name(name) in MONTHLY_SERVICE_TITLES or _normalize_name(name) in MONTHLY_SUBSCRIPTIONS:
            skip_list.append((name, "月費/浮動開支"))
            continue
        if _normalize_name(name) in MONTHLY_INSURANCE_TITLES:
            skip_list.append((name, "月供保險"))
            continue
        if _normalize_name(name) in SKIP_TITLES:
            skip_list.append((name, "已處理/進行中"))
            continue
        if ctype not in REMINDABLE_TYPES:
            skip_list.append((name, f"類型唔需要({ctype})"))
            continue
        
        new_rd = _compute_remind_date(ctype, pay_term, start_str, end_str)
        if new_rd:
            if remind_date_str and remind_date_str == new_rd:
                ok.append((name, new_rd))
            elif remind_date_str:
                need_update.append((name, remind_date_str, new_rd, "更新"))
            else:
                need_update.append((name, "未set", new_rd, "新設"))
        else:
            reason = "缺start/term資料"
            if ctype == "Normal":
                reason = "固定支出"
            elif ctype == "Loan" and not end_str:
                reason = "分期無到期日"
            skip_list.append((name, reason))
    
    print(f"\n✅ 已正確 ({len(ok)}):")
    for name, rd in sorted(ok):
        print(f"   {name:35s} → {rd}")
    
    print(f"\n🔄 需要更新 ({len(need_update)}):")
    for name, old_rd, new_rd, action in sorted(need_update, key=lambda x: x[2]):
        print(f"   {name:35s} {old_rd} → {new_rd} ({action})")
    
    print(f"\n⏸️ 跳過 ({len(skip_list)}):")
    for name, reason in skip_list:
        print(f"   {name:35s} ({reason})")
