---
name: opencode-product-architecture
version: 2
description: 完整產品開發架構指南 — 用 OpenCode (Crush) 由零開發 product。包括完整 OpenCode 系統教學（Antigravity、MyOpenCode、UltraW、Session、Ralph Loop、MCP、GitHub Action）。Terrence 只會提出要求，唔會打 code 或 command。你要預判佢需要咩，自動完成所有 coding/command 工作，並將製成品完美展示。
summary: 完整產品開發架構 + OpenCode 深度教學。Terrence 只提要求，你自動完成一切。
license: Internal
references:
  - references/opencode-full-guide.md
---

# OpenCode Product Architecture Guide

## 核心規則

**Terrence 永遠唔會打 code 或 command。** 佢只會講「我想要XXX」、「幫我做YYY」。你要：
1. 自動拆解需求
2. 自動執行所有 commands
3. 自動生成完整 code
4. 自動 deploy
5. 完美展示製成品俾佢睇（screenshot / live URL / demo）

---

## 2026 標準 Product Tech Stack（10年有效）

```
Backend:      Python 3.13 + FastAPI + SQLAlchemy 2.0 + Alembic
Frontend:     TypeScript 5 + React 19 + Tailwind v4 + shadcn/ui
Database:     PostgreSQL 17 + Redis 8
Auth:         Supabase Auth（Google/Apple login）
Payment:      Stripe
Real-time:    FastAPI WebSocket + Redis Pub/Sub + PG NOTIFY
Container:    Docker + Docker Compose
CI/CD:        GitHub Actions
Monitoring:   Sentry + Prometheus + Grafana
Hosting:      Mac Mini M4 Pro + Cloudflare Tunnel
```

---

## 點解呢個 Stack

| Technology | 原因 | 10年預測 |
|---|---|---|
| Python | AI/ML 霸主，FastAPI 係 2026 標準 | 仲會更強 |
| TypeScript | Industry standard，請人容易 | Standard |
| React | #1 前端框架 | 概念永續 |
| PostgreSQL | 最可靠 open-source DB | 只會更流行 |
| Redis | Cache + Pub/Sub 標準 | Standard |
| Docker | Container 標準 | Standard |
| Mac Mini | $28/mo, silent, 夠力 | 5年回本 |

---

## OpenCode 架構認知

### 四大形態

| 形態 | 用途 |
|---|---|
| **CLI 命令行** | 最核心，所有開發工作 |
| **VS Code 插件** | Alt+Shift+K 送 code 去 AI |
| **Desktop 客戶端** | Beta，基本對話 |
| **GitHub Action** | CI/CD 自動執行 |

### Model 接入策略

| 方案 | 點用 |
|---|---|
| **免費模型** | `/models` 揀 free 標記嘅 model |
| **Antigravity 插件** | 免費接入 Gemini 1.5 Pro / Claude 3.5 Sonnet |
| **OpenRouter** | 俾 API Key 即可用任何 model |

### Session 並行開發

- 每個新對話 = 一個 Session
- `new` = 開新 Session 背景運行
- `/sessions` = 睇所有進行中 task
- `/timeline` = 睇修改記錄，可以 Revert

### 拉爾夫循環 (Ralph Loop)

- 指令：`/r`
- 用途：超複雜任務，AI 自動循環直到完成
- 場景：重構成個 project、全部 test pass

---

## 使用 OpenCode 嘅工作流程

### 當 Terrence 提出要求：

```
Terrence: 「我想要一個 task management system」

你嘅自動流程：
1. 拆解需求 → 決定用咩 tech stack
2. 用 OpenCode CLI 起 project skeleton
3. Generate 晒所有 files
4. 行 dev server
5. 俾 Terrence 睇結果（screenshot / URL）
6. 等 feedback → 再改
```

### 成品展示標準

每次完成後要俾 Terrence 睇到：

1. **Screenshot** — 用 browser 開 localhost cap 圖
2. **Live URL** — 如果有 tunnel，俾條 link
3. **Function List** — 簡單講做到咩
4. **Next Steps** — 問佢想加咩

---

## 常見 Product 模式

### Task Management System
tables: users, tenants, tasks, projects, tags
features: CRUD, filter, sort, drag-drop, real-time
auth: Supabase + RBAC
deploy: Docker Compose on Mac Mini

### Dashboard / Analytics
tables: events, metrics, dashboards
features: charts (recharts), filters, date range, export
real-time: WebSocket push

### AI Agent Platform
tables: agents, conversations, tools, logs
features: multi-agent orchestration, thought streaming
real-time: agent thoughts → WebSocket → dashboard

---

## Mac Mini 部署標準模板

docker-compose.yml 結構：
- postgres:17
- redis:8-alpine
- backend（FastAPI）
- frontend（React + Nginx）
- nginx（reverse proxy）

---

## 展示 Checklist（每次完成都要做）

```
[ ] Server 著咗（local 行到）
[ ] Screenshot cap 咗
[ ] 功能列表準備好
[ ] 問 Terrence 想改咩 / 加咩
[ ] 問要唔要 deploy 去 Mac Mini
```

---

## 10年 Vision Reminder

呢個 stack 係為 product 而設 — 唔係 personal tool。將來：
- Multi-tenant（每個 customer 獨立 data）
- Auth + billing（Stripe）
- Real-time 做 core feature
- AI agents 做 selling point

但而家：prototype first，證實有人 buy 先做 production。
