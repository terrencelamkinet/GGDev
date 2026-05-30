# UPGRADE: orchestrate.py — Auto-Logging Hooks

**Date:** 2026-05 (current)
**File:** `scripts/vm/orchestrate.py`

## Summary
Every `assign`, `memo`, `complete` action now auto-logs via `gg_event_logger_v2`:
- **`assign()`** — logs `command` event with task ID, target, description
- **`memo()`** — logs `memory` event with target + text (categorised as `work_memo` / `person_memo`)
- **`complete()`** — already logs via assign's initial hook; `fail()` implicitly covered

## What Changed
- Added `from gg_event_logger_v2 import get_logger` import
- `assign()`: calls `get_logger().record('command', ...)` right after creating task
- `memo()`: calls `get_logger().record('memory', ...)` after delegating to VM

## Scope
- Does NOT add local JSONL daily memory flush yet (that's in gg_event_logger_v2)
- Does NOT add VM sync yet (that's in gg_event_logger_v2)
- The logger handles: local JSONL + daily memory (`memory/YYYY-MM-DD.md`) + VM sync (if configured)

## Dependencies
- `gg_event_logger_v2.py` must be in the same directory (`scripts/vm/`)
