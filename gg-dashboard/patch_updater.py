#!/usr/bin/env python3
"""Patch hermes_update_data.py to include task data from task_sync_state.json"""
import json, os, sys
from pathlib import Path

BASE = Path.home() / "projects/ggdev-repo/gg-dashboard"
UPDATER = BASE / "hermes_update_data.py"

# Read current updater
content = UPDATER.read_text()

# Check if task injection already exists
if "task_sync_state" in content:
    print("Task data already in updater — checking preservation...")
else:
    print("Adding task data to updater...")

# Find merge_preserved function — add tasks preservation
old_merge = """    # Preserve pushed_at
    if 'pushed_at' in existing:
        new_data['pushed_at'] = existing['pushed_at']"""

new_merge = """    # Preserve pushed_at
    if 'pushed_at' in existing:
        new_data['pushed_at'] = existing['pushed_at']
    # Preserve tasks
    if 'tasks' in existing:
        new_data['tasks'] = existing['tasks']"""

if old_merge in content:
    content = content.replace(old_merge, new_merge)
    print("  + Added tasks field to merge_preserved()")
else:
    print("  ! merge_preserved pattern not found — checking data builder...")

# Find data dict builder — add tasks section
# Look for where data dict is built before json.dump
old_build = """    data = {
        "ts": ts_str,
        "hour": now.hour,
        "minute": now.minute,
        "pushed_at": pushed_at,"""

new_build = """    data = {
        "ts": ts_str,
        "hour": now.hour,
        "minute": now.minute,
        "pushed_at": pushed_at,"""

# Find where costs is added and add tasks after it
old_cost_section = """    # Merge preserved fields
    data = merge_preserved(existing, data)"""

# Actually let me find where the main data object keys are defined
# Read the full file to understand structure better
lines = content.split('\n')
task_section = []
data_section_start = -1
data_section_end = -1

for i, line in enumerate(lines):
    if 'data = {' in line and 'ts' in line:
        # This is likely the main data builder
        # Look backwards for the function that builds the data
        if i > 5 and 'def build_data' in '\n'.join(lines[max(0,i-10):i]):
            data_section_start = i
    if 'data = merge_preserved(existing, data)' in line:
        data_section_end = i

if data_section_end > 0:
    # Add tasks field before merge_preserved
    # Find what's just before it — should be costs or insights
    before_line = data_section_end - 1
    for j in range(data_section_end-1, max(0, data_section_end-10), -1):
        line = lines[j]
        if 'insights' in line or 'costs' in line:
            before_line = j
            break
    
    # Check if tasks already in the data builder
    tasks_in_builder = any('tasks' in line and 'data' in line for line in lines[:data_section_end])
    
    if not tasks_in_builder:
        # Add after the insights/costs line
        ins = ''
        for j in range(before_line, min(len(lines), before_line+5)):
            ins += lines[j] + '\n'
        
        # Find what line to insert after
        # The data object has various fields like costs, insights — we add tasks after the last one before merge
        task_inject = '''\n    # Read tasks from local state file
    tasks_path = os.path.expanduser("~/.hermes/task_sync_state.json")
    if os.path.exists(tasks_path):
        try:
            with open(tasks_path) as tf:
                ts_data = json.load(tf)
            tasks_list = list(ts_data.get("tasks", {}).values())
            # Sort by due date (closest first)
            tasks_list.sort(key=lambda t: t.get("due") or "9999-99-99")
            data["tasks"] = {"items": tasks_list, "total": len(tasks_list), "source": "task_sync_state"}
        except:
            data["tasks"] = {"items": [], "total": 0, "source": "error"}
'''
        
        # Insert tasks after the field before merge_preserved
        before_line_text = lines[before_line]
        # Find a place to insert — after costs or insights but before merge_preserved
        for j in range(before_line, data_section_end):
            l = lines[j]
            if 'data[' in l and '] =' in l:
                last_data_field = j
        
        # Insert after last data field assignment before merge_preserved
        indent = '    '
        task_lines = task_inject.split('\n')
        
        # Insert at data_section_end (right before merge_preserved)
        new_lines = lines[:data_section_end]
        new_lines.append(task_inject)
        new_lines.extend(lines[data_section_end:])
        content = '\n'.join(new_lines)
        print("  + Added tasks section to data builder")
    else:
        print("  + Tasks already in data builder")
else:
    print("  ! Could not find merge_preserved call — manual check needed")

UPDATER.write_text(content)
print("Updater patched successfully")

# Preview the change
with open(UPDATER) as f:
    c = f.read()
if 'task_sync_state' in c:
    # Show the relevant section
    for i, line in enumerate(c.split('\n')):
        if 'task_sync_state' in line or 'tasks_path' in line or 'tasks_list' in line or 'data["tasks"]' in line:
            print(f"  L{i+1}: {line.strip()}")
