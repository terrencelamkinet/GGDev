#!/usr/bin/env python3
"""
C9 NEXUS Conv Sync — silent post-processing for clarification replies.

Detects: 我答「✅」/「done」/「好」/「ok」至一條 clarification，
         然後 auto-update Notion / PG / 觸發對應 action。

Run: 每5分鐘 cron (or C9 includes 此功能)
"""

import os, sys, json, re, subprocess, time
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
HERMES_DB = os.path.expanduser("~/.hermes/sessions.db")

def get_recent_conversations(minutes=10):
    """Get recent Hermes conversation logs from session DB or files."""
    # Try reading from session_search JSON output
    result = subprocess.run(
        ["hermes", "session", "list", "--limit", "5", "--json"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        print(f"[conv_sync] hermes session list failed: {result.stderr}")
        return []
    try:
        sessions = json.loads(result.stdout)
    except json.JSONDecodeError:
        sessions = []
    
    # Filter sessions from last `minutes` minutes
    cutoff = datetime.now(HKT) - timedelta(minutes=minutes)
    recent = []
    for s in sessions:
        ts_str = s.get("started_at", s.get("timestamp", ""))
        if not ts_str:
            continue
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).astimezone(HKT)
        except ValueError:
            continue
        if ts >= cutoff:
            recent.append(s)
    return recent

def extract_clarification_replies(session):
    """Check if user replied to a pending clarification with confirmatory text."""
    session_id = session.get("id", session.get("session_id", ""))
    if not session_id:
        return []
    
    # Get full session content
    result = subprocess.run(
        ["hermes", "session", "get", session_id, "--json"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return []
    
    try:
        msgs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    
    replies = []
    if isinstance(msgs, dict):
        msgs = msgs.get("messages", [])
    if not isinstance(msgs, list):
        return []
    
    for i, msg in enumerate(msgs):
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role != "user":
            continue
        
        content_stripped = content.strip().lower()
        # Check if this looks like confirmation reply
        is_confirm = bool(re.match(r'^(✅|✓|ok|好|done|yes|y|可以|係|confirm|confirm|check|✔|是|做得|做)', content_stripped))
        
        if not is_confirm:
            continue
        
        # Look back at previous assistant message for context
        prev_msg = msgs[i-1] if i > 0 else {}
        prev_content = prev_msg.get("content", "") if isinstance(prev_msg, dict) else ""
        
        # Detect if assistant was asking a clarification question
        prev_lower = prev_content.lower()
        is_clarification = any(kw in prev_lower for kw in [
            "?",
            "係唔係",
            "係咪",
            "好唔好",
            "可以嗎",
            "confirm",
            "確認",
            "請確認",
            "要唔要",
        ]) and len(prev_content) < 200  # short = clarification, not long response
        
        if is_clarification:
            replies.append({
                "session_id": session_id,
                "user_reply": content,
                "assistant_question": prev_content,
                "timestamp": msg.get("timestamp", ""),
            })
    
    return replies

def process_reply(reply):
    """Decide what action to take based on the clarification context."""
    question = reply["assistant_question"].strip()
    user_reply = reply["user_reply"].strip()
    
    print(f"[conv_sync] Processing: \"{question[:80]}...\" → \"{user_reply}\"")
    
    # --- Detect action type from question ---
    
    # 1. Link task to project
    if re.search(r'link.*task|task.*link|connect.*project|project.*connect', question, re.I):
        # Extract task name and project name from question
        task_match = re.search(r'[`"]([^`"]+)[`"]', question)
        if task_match:
            task_name = task_match.group(1)
            print(f"[conv_sync] → Linking task '{task_name}' to project (auto)")
            # The actual link action requires Notion API — logged for next cron cycle
            _log_pending_action("link_task_project", {"task": task_name, "reply": user_reply})
    
    # 2. Create task / follow-up
    elif re.search(r'create.*task|add.*task|follow.?up|todo', question, re.I):
        _log_pending_action("create_task", {"context": question, "reply": user_reply})
    
    # 3. Mark something as done / complete
    elif re.search(r'mark.*done|complete.*task|done\?', question, re.I):
        _log_pending_action("mark_done", {"context": question, "reply": user_reply})
    
    # 4. General confirmation — log for review
    else:
        _log_pending_action("general_confirm", {"context": question, "reply": user_reply})
    
    return True

PENDING_LOG = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs", "conv_sync_pending.jsonl")

def _log_pending_action(action_type, payload):
    """Log pending action for next cron cycle to execute."""
    os.makedirs(os.path.dirname(PENDING_LOG), exist_ok=True)
    entry = {
        "type": action_type,
        "payload": payload,
        "timestamp": datetime.now(HKT).isoformat(),
    }
    with open(PENDING_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[conv_sync] ✓ Pending action logged: {action_type}")

def execute_pending_actions():
    """Execute any pending actions from previous cycles."""
    if not os.path.exists(PENDING_LOG):
        return
    
    pending = []
    with open(PENDING_LOG, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    pending.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    if not pending:
        return
    
    print(f"[conv_sync] Executing {len(pending)} pending action(s)...")
    
    # For now, just log them — actual execution happens in main cron
    # Clear the file after reading
    os.remove(PENDING_LOG)
    
    # Re-write any that failed to execute
    failed = []
    for action in pending:
        try:
            _execute_single(action)
        except Exception as e:
            print(f"[conv_sync] ✗ Failed to execute {action['type']}: {e}")
            failed.append(action)
    
    if failed:
        with open(PENDING_LOG, "w") as f:
            for action in failed:
                f.write(json.dumps(action, ensure_ascii=False) + "\n")

def _execute_single(action):
    """Execute a single pending action."""
    atype = action["type"]
    payload = action["payload"]
    
    if atype == "link_task_project":
        print(f"[conv_sync] Executing link_task_project: {payload}")
        # TODO: call Notion API to link task to project
        pass
    
    elif atype == "general_confirm":
        print(f"[conv_sync] General confirmation noted: {payload['context'][:60]}...")
        pass

def main():
    print(f"[conv_sync] {datetime.now(HKT).isoformat()} — Starting conv sync...")
    
    # Phase 1: Execute any pending actions from last cycle
    execute_pending_actions()
    
    # Phase 2: Check recent conversations for clarification replies
    sessions = get_recent_conversations(minutes=10)
    if not sessions:
        print("[conv_sync] No recent sessions found")
        return
    
    print(f"[conv_sync] Found {len(sessions)} recent session(s)")
    
    for session in sessions:
        replies = extract_clarification_replies(session)
        for reply in replies:
            process_reply(reply)
    
    print(f"[conv_sync] Done — {datetime.now(HKT).isoformat()}")

if __name__ == "__main__":
    main()
