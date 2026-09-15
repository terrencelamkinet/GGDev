#!/usr/bin/env python3
"""
gg_insights_pusher.py — Push new stacking insights to Telegram.

RUNS: Every 15 min via cron (after collector)
PURPOSE: Check if new entries since last push, format push message, save push log.
  - Only pushes genuinely new entries (not repeats)
  - Groups by source for readability
  - Skips trivial/noise entries
"""

import json, os, datetime
from pathlib import Path

HKT = datetime.timezone(datetime.timedelta(hours=8))
NOW = datetime.datetime.now(HKT)

BASE = Path.home() / "projects/ggdev-repo/gg-dashboard"
INSIGHTS_FILE = BASE / "gg-insights.json"
PUSH_LOG = BASE / "gg-insights-pushlog.json"

# Entry types that are worth pushing
PUSHABLE_TYPES = {"discovery", "trend", "suggestion", "milestone"}
# Skip these messages (too noisy)
SKIP_PATTERNS = ["Cron output:", "無 urgent", "沒有新發現", "所有 daemon 正常", "已穩定運行"]

def should_push(entry):
    """Filter: skip noise, only push meaningful entries."""
    msg = entry.get("msg", "")
    for pat in SKIP_PATTERNS:
        if pat in msg:
            return False
    entry_type = entry.get("type", "")
    if entry_type in PUSHABLE_TYPES:
        return True
    if entry_type == "activity" and entry.get("source") in ("work", "person"):
        return True  # Push work/person activity
    return False

def main():
    insights = {}
    try:
        with open(INSIGHTS_FILE) as f:
            insights = json.load(f)
    except:
        print("NO_DATA")
        return

    push_log = {"last_push_id": 0, "pushed": []}
    if PUSH_LOG.exists():
        try:
            with open(PUSH_LOG) as f:
                push_log = json.load(f)
        except:
            pass

    last_push_id = push_log.get("last_push_id", 0)
    entries = insights.get("entries", [])

    # Find new entries that haven't been pushed
    new_entries = [e for e in entries if e.get("id", 0) > last_push_id and should_push(e)]

    if not new_entries:
        print("NOTHING_NEW")
        return

    # Group by source for readable push
    by_source = {}
    for e in new_entries:
        src = e.get("source", "system")
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(e)

    # Build push message
    src_labels = {
        "fighter": "🤖 GG Fighter",
        "work": "⚙️ GG-Work",
        "person": "❤️ GG-Person",
        "system": "🔧 System"
    }
    type_icons = {"activity": "📋", "discovery": "🔍", "trend": "📊", "suggestion": "🎯", "milestone": "✨"}

    lines = [f"🧠 GG Intelligence Update", f"───", f""]
    for source in ["fighter", "work", "person", "system"]:
        if source in by_source:
            lines.append(f"**{src_labels.get(source, source)}**")
            for e in by_source[source]:
                icon = type_icons.get(e.get("type", ""), "📌")
                lines.append(f"├ {icon} {e.get('msg', '')}")
            lines.append("")

    lines.append(f"📊 {len(new_entries)} new — {len(entries)} total")

    # Save push log
    max_id = max(e.get("id", 0) for e in new_entries)
    push_log["last_push_id"] = max_id
    push_log["pushed"].append({
        "ts": NOW.strftime("%Y-%m-%d %H:%M"),
        "count": len(new_entries),
        "max_id": max_id
    })
    # Keep last 50 push records
    if len(push_log["pushed"]) > 50:
        push_log["pushed"] = push_log["pushed"][-50:]

    with open(PUSH_LOG, "w") as f:
        json.dump(push_log, f, indent=2, ensure_ascii=False)

    # Output for cron delivery
    print("\n".join(lines))

if __name__ == "__main__":
    main()
