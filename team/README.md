# Agent Team Directory — GG Multi-Agent System

## Overview
呢個係 GG 三部機嘅 shared workspace，用 agent-team-orchestration 模式管理任務。

## Directory Structure

```
team/
├── README.md        ← 呢個 file
├── inbox/           ← 新任務 inbox（未分配）
├── tasks/           ← 已分配任務（orchestrate.py 管理）
├── artifacts/       ← 完成嘅 deliverables
├── decisions/       ← 重要決策記錄
└── reviews/         ← 跨機 review comments
```

## Task File Format

每條 task 用 JSON 格式，跟 orchestrate.py 嘅 lifecycle：

```json
{
  "tid": "0001",
  "target": "work|person",
  "status": "assigned|in_progress|review|done|failed",
  "desc": "Task description",
  "assigned_at": "ISO8601",
  "completed_at": null,
  "artifact": null,
  "handoff": {"action": "...", "output": "..."},
  "comments": [
    {"by": "gg-main", "at": "ISO8601", "msg": "comment"}
  ]
}
```

## Task Lifecycle States

```
Inbox ──→ Assigned ──→ In Progress ──→ Review ──→ Done
                   ↘                               ↗
                     └────── Failed ←─────────────┘
```

## Shared Artifacts Paths

- GG-Work 產出 → `artifacts/work-{tid}.md`
- GG-Person 產出 → `artifacts/person-{tid}.md`

## Decision Records

`decisions/` 放重要決策，格式：
- `YYYY-MM-DD_title.md`
- 包含：decision, rationale, alternatives considered

## Review Workflow

- Builder 完成 task → status → `review`
- Review 記錄寫入 `reviews/`
- Orchestrator (main GG) 驗證 → pass: done, fail: back to assigned

## 連通

- Main GG 直接存取本地 team/
- GG-Work / GG-Person 通過 VM query ($quest) 存取
- Sync agent 每15分鐘更新 cross-machine events
