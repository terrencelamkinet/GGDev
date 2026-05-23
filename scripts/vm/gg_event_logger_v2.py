#!/usr/bin/env python3
"""
GG Master Log Daemon (v2) — 三部機統一紀錄系統

參考:
- Agent Team Orchestration: shared workspace + task lifecycle + handoff protocol
- Self-Improvement Skill: structured learnings with ID/priority/status
- Capability Evolver: pattern detection from log analytics

Core Principles:
1. 每部機獨立紀錄 → 但格式統一 → 可以 cross-reference
2. 每次操作自動留底 → timestamp + source + category
3. 每次關鍵事件 sync 去其他 VM → 大家知道對方做咩
4. 每日 summary → 自動 extract 俾 main GG 用

Storage:
  ~/.openclaw/logs/gg-v2/
  ├── events.jsonl       # 所有事件（每次操作一條）
  ├── handoffs.jsonl     # 跨機溝通記錄（A→B 做咗咩）
  ├── heartbeats.jsonl   # 定時 health check
  └── daily/             # 每日 summary
      └── YYYY-MM-DD.md

Format (JSONL):
{
  "ts": "ISO8601",
  "host": "gg-main|gg-work|gg-person",
  "level": "INFO|WARN|ERROR|FATAL",
  "event_id": "EVT-20260520-001",
  "category": "conversation|upgrade|communication|connection|cron|error|config|command|system|memory",
  "source": "orchestrate|vm_query|cron|manual|auto",
  "message": "human readable summary",
  "details": { "optional structured data" },
  "handoff": { "to": "gg-work|gg-person", "status": "pending|done|failed" }  # 如果有跨機
}
"""
import json, os, sys, socket, uuid, logging, logging.handlers
from datetime import datetime, timezone, timedelta
from pathlib import Path

HOSTNAME = socket.gethostname()
HOST_ALIAS = {
    "arpa-ai-test01": "gg-main",
    "vps-work": "gg-work",
    "vps-person": "gg-person"
}.get(HOSTNAME, HOSTNAME)

LOG_DIR = os.path.expanduser("~/.openclaw/logs/gg-v2")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
TEAM_DIR = os.path.expanduser("~/.openclaw/workspace/team")

# Daily event counter for ID generation
_event_counter = 0

class GGEventLogger:
    """Unified event logger — every operation gets recorded"""
    
    def __init__(self):
        self._ensure_dirs()
        self._init_handlers()
    
    def _ensure_dirs(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(os.path.join(LOG_DIR, "daily"), exist_ok=True)
        os.makedirs(MEMORY_DIR, exist_ok=True)
    
    def _init_handlers(self):
        """Setup dual logging: console + JSONL"""
        self.logger = logging.getLogger(f"gg.{HOST_ALIAS}")
        self.logger.setLevel(logging.DEBUG)
        
        if self.logger.handlers:
            return
        
        # Text log for human reading
        txt_handler = logging.handlers.RotatingFileHandler(
            os.path.join(LOG_DIR, f"{HOST_ALIAS}.log"),
            maxBytes=5*1024*1024, backupCount=3
        )
        txt_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        ))
        self.logger.addHandler(txt_handler)
    
    def _next_event_id(self):
        now = datetime.now()
        return f"EVT-{now.strftime("%Y%m%d")}-{now.strftime("%H%M%S")}"
    
    def _get_host_alias(self):
        return HOST_ALIAS
    
    def record(self, category, message, level="INFO", details=None, handoff=None, source="auto"):
        """
        Record ONE event. This is the single entry point for all logging.
        
        Args:
            category: conversation|upgrade|communication|connection|cron|error|config|command|system|memory
            message: human readable summary (max 500 chars)
            level: INFO|WARN|ERROR|FATAL
            details: optional dict with structured data
            handoff: optional dict {"to": "gg-work|gg-person", "status": "pending|done|failed"}
            source: orchestrate|vm_query|cron|manual|auto
        """
        event_id = self._next_event_id()
        ts = datetime.now(timezone.utc).isoformat()
        ts_hkt = datetime.now().strftime("%H:%M HKT")
        today = datetime.now().strftime("%Y-%m-%d")
        
        entry = {
            "ts": ts,
            "host": self._get_host_alias(),
            "level": level.upper(),
            "event_id": event_id,
            "category": category,
            "source": source,
            "message": message[:500],
            "date": today
        }
        if details:
            entry["details"] = details
        if handoff:
            entry["handoff"] = handoff
        
        # 1. Write to JSONL events file
        events_file = os.path.join(LOG_DIR, "events.jsonl")
        try:
            with open(events_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to write events.jsonl: {e}")
        
        # 2. Write to daily memory file
        mem_file = os.path.join(MEMORY_DIR, f"{today}.md")
        try:
            cat_emoji = {
                "conversation": "💬", "upgrade": "⬆️", "communication": "📡",
                "connection": "🔗", "cron": "⏰", "error": "❌",
                "config": "⚙️", "command": "⌨️", "system": "🖥️", "memory": "🧠"
            }.get(category, "📝")
            
            if handoff:
                arrow = "→" if handoff.get("to") else "↔"
                handoff_str = f" {arrow} {handoff['to']}"
            else:
                handoff_str = ""
            
            line = f"\n- **{ts_hkt}** {cat_emoji} **[{category.upper()}]** `{event_id}`{handoff_str} {message}"
            
            if not os.path.exists(mem_file):
                with open(mem_file, "w") as f:
                    f.write(f"# {today}\n")
            
            with open(mem_file, "a") as f:
                f.write(line)
        except Exception as e:
            self.logger.error(f"Failed to write memory file: {e}")
        
        # 3. If this is a handoff event, write to handoffs.jsonl
        if handoff:
            try:
                handoff_file = os.path.join(LOG_DIR, "handoffs.jsonl")
                with open(handoff_file, "a") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            except Exception as e:
                self.logger.error(f"Failed to write handoffs.jsonl: {e}")
        
        # 4. Console log
        self.logger.info(f"[{category}] {message[:200]}")
        
        return event_id
    
    def heartbeat(self, status="healthy", details=None):
        """Record a periodic health check"""
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "host": self._get_host_alias(),
            "status": status,
            "details": details or {}
        }
        hb_file = os.path.join(LOG_DIR, "heartbeats.jsonl")
        try:
            with open(hb_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass
    
    def get_events(self, limit=50, category=None, host=None, since=None):
        """Read recent events from the JSONL file"""
        events = []
        events_file = os.path.join(LOG_DIR, "events.jsonl")
        
        if not os.path.exists(events_file):
            return events
        
        try:
            with open(events_file) as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        evt = json.loads(line)
                        if category and evt.get("category") != category: continue
                        if host and evt.get("host") != host: continue
                        if since:
                            evt_ts = datetime.fromisoformat(evt["ts"])
                            if evt_ts < since: continue
                        events.append(evt)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
        
        return events[-limit:]
    
    def get_handoffs(self, limit=20):
        """Read recent handoff events"""
        events = []
        handoff_file = os.path.join(LOG_DIR, "handoffs.jsonl")
        
        if not os.path.exists(handoff_file):
            return events
        
        try:
            with open(handoff_file) as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
        
        return events[-limit:]

# Singleton
_instance = None

def get_logger():
    global _instance
    if _instance is None:
        _instance = GGEventLogger()
    return _instance


# ===== CLI Interface =====
def cli():
    import argparse
    parser = argparse.ArgumentParser(description="GG Event Logger v2")
    parser.add_argument("action", choices=["record", "heartbeat", "check", "recent"])
    
    # record
    parser.add_argument("--category", choices=[
        "conversation","upgrade","communication","connection",
        "cron","error","config","command","system","memory"
    ])
    parser.add_argument("--message", help="what happened")
    parser.add_argument("--level", choices=["INFO","WARN","ERROR","FATAL"], default="INFO")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--details", help="JSON details")
    parser.add_argument("--handoff-to", help="handoff target: gg-work|gg-person")
    parser.add_argument("--handoff-status", choices=["pending","done","failed"], default="done")
    
    # check/recent
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--filter-host", help="filter by host")
    parser.add_argument("--filter-category", help="filter by category")
    
    args = parser.parse_args()
    
    log = get_logger()
    
    if args.action == "record":
        if not args.category or not args.message:
            print(json.dumps({"error": "category and message required for record"}))
            sys.exit(1)
        
        details = json.loads(args.details) if args.details else None
        handoff = None
        if args.handoff_to:
            handoff = {"to": args.handoff_to, "status": args.handoff_status}
        
        event_id = log.record(
            category=args.category,
            message=args.message,
            level=args.level,
            details=details,
            handoff=handoff,
            source=args.source
        )
        print(json.dumps({"event_id": event_id, "host": HOST_ALIAS}))
    
    elif args.action == "heartbeat":
        log.heartbeat()
        print(json.dumps({"ok": True, "host": HOST_ALIAS}))
    
    elif args.action in ("check", "recent"):
        events = log.get_events(
            limit=args.limit,
            category=args.filter_category,
            host=args.filter_host
        )
        print(json.dumps(events, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
