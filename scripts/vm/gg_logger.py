#!/usr/bin/env python3
"""
GG Unified Logger — 三部機統一日誌系統 (v1)

記錄所有操作：對話、升級、溝通、連接、cron jobs、errors
每部機獨立記錄，但格式統一，方便 cross-reference

Log levels:
  INFO  — 正常操作
  WARN  — 異常但唔影響運作
  ERROR — 需要關注嘅問題
  FATAL — 需要即時處理

Storage:
  /var/log/gg/  — 系統層 logs (rotated weekly)
  ~/.openclaw/logs/gg/  — 應用層 logs

Format (JSONL):
  {"ts":"ISO8601","host":"...","level":"...","source":"...","message":"...","details":{...}}
"""
import json, os, sys, socket, logging, logging.handlers
from datetime import datetime, timezone

LOG_DIR = "/var/log/gg"
APP_LOG_DIR = os.path.expanduser("~/.openclaw/logs/gg")
HOSTNAME = socket.gethostname()

class GGLogger:
    """Unified logger for all 3 GG machines"""
    
    def __init__(self, source="gg-main"):
        self.source = source
        self._ensure_dirs()
        self._setup_handlers()
    
    def _ensure_dirs(self):
        for d in [LOG_DIR, APP_LOG_DIR]:
            try:
                os.makedirs(d, exist_ok=True)
                os.chmod(d, 0o755)
            except PermissionError:
                # Fallback to app log dir
                os.makedirs(APP_LOG_DIR, exist_ok=True)
    
    def _setup_handlers(self):
        """Setup dual logging: system log + app log"""
        self.logger = logging.getLogger(f"gg.{self.source}")
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if self.logger.handlers:
            return
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # System log (rotated weekly)
        sys_log = os.path.join(LOG_DIR, f"{self.source}.log")
        try:
            handler = logging.handlers.TimedRotatingFileHandler(
                sys_log, when='W6', interval=1, backupCount=4  # Weekly rotate, keep 4 weeks
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.INFO)
            self.logger.addHandler(handler)
        except PermissionError:
            pass  # Skip system log if no permission
        
        # App log (always available)
        app_log = os.path.join(APP_LOG_DIR, f"{self.source}.log")
        app_handler = logging.handlers.RotatingFileHandler(
            app_log, maxBytes=5*1024*1024, backupCount=3  # 5MB rotate
        )
        app_handler.setFormatter(formatter)
        app_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(app_handler)
        
        # JSONL structured log (for machine parsing)
        jsonl_path = os.path.join(APP_LOG_DIR, f"{self.source}.jsonl")
        self.jsonl_file = jsonl_path
    
    def _jsonl(self, level, message, details=None):
        """Write structured JSONL entry"""
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "host": HOSTNAME,
                "source": self.source,
                "level": level,
                "message": message
            }
            if details:
                entry["details"] = details
            
            with open(self.jsonl_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass  # Don't let logging fail the app
    
    def info(self, message, details=None):
        self.logger.info(message)
        self._jsonl("INFO", message, details)
    
    def warn(self, message, details=None):
        self.logger.warning(message)
        self._jsonl("WARN", message, details)
    
    def error(self, message, details=None):
        self.logger.error(message)
        self._jsonl("ERROR", message, details)
    
    def fatal(self, message, details=None):
        self.logger.critical(message)
        self._jsonl("FATAL", message, details)

    def memory_record(self, category, content):
        """
        Record a memory-worthy event. 
        This is the key method that ensures every significant action gets logged.
        """
        self.info(f"MEMORY|{category}|{content[:200]}")
        
        # Also write to the daily memory file
        today = datetime.now().strftime("%Y-%m-%d")
        mem_file = os.path.join(
            os.path.expanduser("~/.openclaw/workspace/memory"),
            f"{today}.md"
        )
        try:
            ts = datetime.now().strftime("%H:%M HKT")
            with open(mem_file, "a") as f:
                f.write(f"\n- **{ts}** [{category}] {content}")
        except Exception:
            pass

# Singleton
_instances = {}

def get_logger(source="gg-main"):
    if source not in _instances:
        _instances[source] = GGLogger(source)
    return _instances[source]

if __name__ == "__main__":
    # CLI mode: gg_logger.py <source> <level> <message> [--json details]
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="log source name")
    parser.add_argument("level", choices=["info","warn","error","fatal","memory"])
    parser.add_argument("message", help="log message")
    parser.add_argument("--details", help="JSON details")
    parser.add_argument("--category", help="category for memory records")
    args = parser.parse_args()
    
    log = get_logger(args.source)
    details = json.loads(args.details) if args.details else None
    
    if args.level == "memory":
        cat = args.category or "general"
        log.memory_record(cat, args.message)
    elif args.level == "info":
        log.info(args.message, details)
    elif args.level == "warn":
        log.warn(args.message, details)
    elif args.level == "error":
        log.error(args.message, details)
    elif args.level == "fatal":
        log.fatal(args.message, details)
    
    print(json.dumps({"ok": True}))
