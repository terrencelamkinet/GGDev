#!/usr/bin/env python3
"""
GG Log Analyzer — 分析 events.jsonl 俾出 insights

參考:
- Capability Evolver: detect error patterns from log analytics
- Self-Improvement: structured learnings with ID/priority/status

Usage:
  python3 gg_log_analyzer.py [--hours 24] [--threshold 0.1]

Output:
  - Health score (0-1)
  - Error rate by category
  - Most frequent patterns
  - Recommendations if score < threshold
"""
import json, os, sys
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

LOG_DIR = os.path.expanduser("~/.openclaw/logs/gg-v2")
LEARNINGS_DIR = os.path.expanduser("~/.openclaw/workspace/.learnings")

# Error weight for health score
ERROR_WEIGHTS = {
    "FATAL": 1.0,
    "ERROR": 0.6,
    "WARN": 0.2,
    "INFO": 0.0
}

def load_events(hours=24):
    """Load events from last N hours"""
    events = []
    events_file = os.path.join(LOG_DIR, "events.jsonl")
    
    if not os.path.exists(events_file):
        return events
    
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    with open(events_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                evt = json.loads(line)
                evt_ts = datetime.fromisoformat(evt["ts"])
                if evt_ts >= cutoff:
                    events.append(evt)
            except (json.JSONDecodeError, ValueError):
                continue
    
    return events

def analyze(events):
    """Analyze events and produce health report"""
    total = len(events)
    if total == 0:
        return {"score": 1.0, "message": "No events in period", "ok": True}
    
    # Category breakdown
    categories = Counter(e.get("category", "unknown") for e in events)
    levels = Counter(e.get("level", "INFO") for e in events)
    
    # Error analysis
    errors = [e for e in events if e.get("level") in ("ERROR", "FATAL")]
    warns = [e for e in events if e.get("level") == "WARN"]
    
    error_penalty = sum(ERROR_WEIGHTS.get(e.get("level", "INFO"), 0) for e in events)
    health_score = max(0, 1.0 - (error_penalty / max(total, 1)))
    
    # Pattern detection: repeated messages
    msg_counter = Counter(e.get("message", "")[:80] for e in errors)
    top_errors = msg_counter.most_common(3)
    
    return {
        "score": round(health_score, 3),
        "total_events": total,
        "error_count": len(errors),
        "warn_count": len(warns),
        "categories": dict(categories.most_common()),
        "top_errors": [{"msg": m, "count": c} for m, c in top_errors if c > 1],
        "ok": health_score >= 0.8
    }

def log_learnings(report):
    """Log significant findings to .learnings/ERRORS.md"""
    if report["error_count"] == 0 and report["warn_count"] == 0:
        return
    
    errors_file = os.path.join(LEARNINGS_DIR, "ERRORS.md")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    with open(errors_file, "a") as f:
        f.write(f"\n## {ts} — Log Analysis Report\n")
        f.write(f"- Health Score: {report['score']}\n")
        f.write(f"- Errors: {report['error_count']}, Warnings: {report['warn_count']}\n")
        if report["top_errors"]:
            f.write("- Top Repeating Errors:\n")
            for e in report["top_errors"]:
                f.write(f"  - \"{e['msg']}\" ({e['count']}x)\n")
        f.write("\n")

def cli():
    import argparse
    parser = argparse.ArgumentParser(description="GG Log Analyzer")
    parser.add_argument("--hours", type=int, default=24, help="Analysis window in hours")
    parser.add_argument("--threshold", type=float, default=0.8, help="Health score threshold")
    args = parser.parse_args()
    
    events = load_events(hours=args.hours)
    report = analyze(events)
    
    print(f"📊 GG Log Analysis (last {args.hours}h)")
    print(f"═════════════════════════════")
    print(f"Health Score: {'🟢' if report['ok'] else '🔴'} {report['score']}")
    print(f"Total Events: {report['total_events']}")
    print(f"Errors: {report['error_count']}  Warnings: {report['warn_count']}")
    print(f"\nCategories:")
    for cat, count in report.get("categories", {}).items():
        emoji = {"config":"⚙️","memory":"🧠","system":"🖥️","upgrade":"⬆️","command":"⌨️","error":"❌","conversation":"💬","communication":"📡","connection":"🔗","cron":"⏰"}.get(cat,"📝")
        print(f"  {emoji} {cat}: {count}")
    
    if report["top_errors"]:
        print(f"\n⚠️ Repeated Errors:")
        for e in report["top_errors"]:
            print(f"  ✗ \"{e['msg']}\" ({e['count']}x)")
    
    if not report['ok']:
        print(f"\n🔴 Health below threshold ({args.threshold}).")
        print("  → Check .learnings/ERRORS.md for details")
        print("  → Consider running capability-evolver if available")
        log_learnings(report)
    else:
        print(f"\n🟢 System healthy")
    
    print(f"\nReport: {'✅ Written to ERRORS.md' if not report['ok'] else '✅ No action needed'}")

if __name__ == "__main__":
    cli()
