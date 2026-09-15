# Task Hub Smart v2 — PostgreSQL-Driven 智能設計

> 設計目標：用 PostgreSQL 做智慧決策，唔靠 LLM，零 token 成本

---

## 1. 現狀問題

- Priority 係 static label (P0/P1)，唔反映真實 urgency
- Push 係 fixed schedule，唔理你而家做緊咩
- 冇 learning loop，唔知你咩時候睇咩時候 skip
- Task 之間冇 dependency tracking
- 唔知你 calendar 有冇空檔

## 2. PostgreSQL 可以做嘅 Smart Features

### 2.1 Smart Urgency Score (純 SQL)

新 column: `urgency_score DECIMAL(5,2)`，由 trigger 每小時 recalculate。

Formula:
- deadline proximity (0-0.4): (24 - hours_until_due) / 24 * 0.4
- blocker weight (0-0.2): blocked_by_count * 0.2
- Ivy 6 bonus (0.3): is_ivy6_today ? 0.3 : 0
- Calendar slot (-0.1): has_free_slot ? -0.1 : 0

### 2.2 Context-Aware Push (script + SQL)

Push 內容 dynamic，唔係 hardcode format：
- Morning: only today's decisions + overdue Ivy 6
- Midday: short tasks you can fit in calendar gaps
- Commute: things to decide tonight + family reminders
- Evening: what's rolling to tomorrow

### 2.3 Completion Pattern Learning

New table `completion_stats` collects:
- day_of_week, hour_bucket
- task_type (quick/medium/deep)
- completion_rate (done vs deferred)
- avg_duration_min

Push 時用 pattern 調整語氣同 timing。

### 2.4 Dependency Graph

`tasks.parent_task_id` + recursive CTE for blocker chain detection.
Auto-escalate blocked high-priority tasks.

### 2.5 Overdue Auto-Escalation

Nightly PG job bumps priority of overdue tasks (P3→P2, P2→P1).
Notes field gets auto-log entry.

## 3. Key Decisions

- All logic in SQL/script — ¥0 incremental cost
- PG trigger for scoring — auto-recalculate on task update
- Push format determined by query results, not hardcode
- Learning from stats, not LLM
