***REMOVED***!/bin/bash
***REMOVED*** memory.sh — Thin dispatcher for Agent Brain v4
***REMOVED*** Routes all commands to brain.py (Python engine with pluggable storage)
***REMOVED***
***REMOVED*** Usage: ./scripts/memory.sh <command> [args]
***REMOVED***
***REMOVED*** Environment:
***REMOVED***   MEMORY_DIR           Path to memory directory (default: ../memory)
***REMOVED***   AGENT_BRAIN_BACKEND  Storage backend: 'sqlite' (default) or 'json'
***REMOVED***   AGENT_BRAIN_SUPERMEMORY_SYNC  SuperMemory sync mode: auto|on|off
***REMOVED***   AGENT_BRAIN_PII_MODE PII policy: strict (default) | off
***REMOVED***   SUPERMEMORY_API_KEY  Optional API key for cloud mirror
***REMOVED***   AGENT_BRAIN_ENV_FILE Optional local env file (default: ../.env)
***REMOVED***
***REMOVED*** Core Commands:
***REMOVED***   init                                              Initialize memory
***REMOVED***   add <type> <content> [source] [tags] [url] [ctx]  Add an entry
***REMOVED***   get <query> [--policy] [--stores] [--explain]    Hybrid retrieval
***REMOVED***   loop <message> [--user-feedback] [--response] [--policy] [--stores] Orchestrated retrieve/extract/learn
***REMOVED***   list [type]                                       List all or by type
***REMOVED***   update <id> <field> <value>                       Update a field on an entry
***REMOVED***   touch <id>                                        Mark as accessed
***REMOVED***   supersede <old_id> <new_id>                       Mark entry as superseded
***REMOVED***
***REMOVED*** Learning Commands:
***REMOVED***   conflicts <content>                               Find potential conflicts
***REMOVED***   similar <content> [threshold]                     Find related entries (TF-IDF)
***REMOVED***   correct <wrong_id> <right> [reason] [tags]        Track a correction
***REMOVED***   success <id> [context]                            Record successful use
***REMOVED***
***REMOVED*** Analysis Commands:
***REMOVED***   reflect                                           Memory health analysis
***REMOVED***   consolidate                                       Find consolidation candidates
***REMOVED***   tags                                              List tag hierarchy
***REMOVED***   decay                                             Downgrade stale entries
***REMOVED***   export                                            Dump full JSON
***REMOVED***   stats                                             Memory statistics
***REMOVED***   log [count] [action]                               Activity log
***REMOVED***
***REMOVED*** Session Commands:
***REMOVED***   session [context]                                 Start new session

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export MEMORY_DIR="${MEMORY_DIR:-$(cd "$SCRIPT_DIR/../memory" && pwd 2>/dev/null || echo "$SCRIPT_DIR/../memory")}"

***REMOVED*** Optional local env auto-load for standalone skill packaging.
if [[ -z "${SUPERMEMORY_API_KEY:-}" ]]; then
  SUPERMEMORY_ENV="${AGENT_BRAIN_ENV_FILE:-$SCRIPT_DIR/../.env}"
  if [[ -f "$SUPERMEMORY_ENV" ]]; then
    parsed_key="$(python3 - "$SUPERMEMORY_ENV" <<'PY'
import sys

path = sys.argv[1]
value = ""
with open(path, "r", encoding="utf-8") as fh:
    for raw in fh:
        line = raw.strip()
        if not line or line.startswith("***REMOVED***") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        if key != "SUPERMEMORY_API_KEY":
            continue
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        value = val
        break
print(value)
PY
)"
    if [[ -n "$parsed_key" ]]; then
      export SUPERMEMORY_API_KEY="$parsed_key"
    fi
  fi
fi

exec python3 "$SCRIPT_DIR/brain.py" "$@"
