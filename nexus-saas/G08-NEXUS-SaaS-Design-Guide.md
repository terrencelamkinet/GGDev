# NEXUS CRM — SaaS Platform Design Guide

> 基於 G08 NEXUS CRM v2 核心系統，設計一個支援 100 個獨立帳戶嘅 SaaS CRM 平台。
> 呢份文件分三部分：(A) 完整功能目錄 (B) 核心架構原則 (C) AI Web Layout Design Guide

---

## A — 完整功能目錄

### CRM Core（數據層）

| 功能 | 說明 | 數據源 |
|------|------|--------|
| Companies | 名稱、行業、分類、電話、地址、健康評分 | 用戶輸入 / 自動 sync |
| Contacts | 姓名、職位、電話、電郵、所屬公司、社交 links | 用戶輸入 / 名卡 scan |
| Deals / Projects | 項目名、所屬公司、階段（Proposal/Negotiate/PO/Delivery/Closed Won/Lost）、金額、probability、closed date | 用戶輸入 |
| Products | 產品名、品牌、類別、價格 band、short pitch、datasheet URL | 用戶輸入 |
| Touchpoints | Meeting/Call/Email/Briefing/Workshop/Outreach 時間線，自動記錄 | 自動+手動 |
| Tasks | P0-P3 優先級、Due date、Eisenhower Matrix 象限、關聯 project | 用戶輸入 / 自動 create |

### Meeting Intelligence Layer（自動收集）

| 功能 | 觸發頻率 | 說明 |
|------|---------|------|
| Calendar Sync | 每15分鐘 | Fetch Google Calendar events |
| Event Classification（14種） | 每15分鐘 | POC/Demo/Client Meal/Workshop/Exam/Course/Vendor/Client Online/Internal/Personal/Church 等 |
| CRM Sync | 每30分鐘 | 雙向 sync（companies/contacts/projects/touchpoints/tasks） |
| NameCard Scanner | 每日10:00（可配置） | Upload image → LLM Vision corner detect → OCR → OpenCV enhance → auto-create contact |
| Entity Matcher | 每15分鐘 | Event title → company/contact automatic lookup |

### AI Intelligence Layer（LLM，按需）

| 功能 | 觸發 | 輸出 |
|------|------|------|
| Meeting Brief | Meeting前5-25分鐘 | 7維度 AI analysis：目的、與會者、背景、關鍵議題、商機、風險、建議 |
| Deal Radar | 可配置 daily | Per project health score + risk flag + next step suggestion |
| Health Scoring | 每日04:00 | Company health score（touchpoint frequency + project progress + recency） |
| Relationship Coach | 每週 | 提醒過期未聯絡客戶，建議 outreach |
| Proactive Gap Detection | 每15分鐘 | Detect missing company/contacts in upcoming events → ask user to fill |

### Notification Layer

| 功能 | 時間 | 格式示例 |
|------|------|---------|
| 60-min Pre-meeting Nudge | Event前55-65分鐘 | 「🤝 60分鐘後: Title · 🏢 Company · 👥 Contacts」 |
| 15-min Pre-meeting Nudge | Event前10-20分鐘 | 「🤝 11分鐘後: Title · 📍 Location」 |
| Post-meeting Touchpoint | 完會後60-120分鐘 | 問「邊個參與？」→ 自動 create touchpoint + follow-up task |
| Clock-in | 09:00 | 天氣 + 今日行程 |
| Night Review | 23:00 | 今日回顧 + 明日 preview + 聽日天氣 |
| Tasks Summary | 07:35 | 7天內 tasks 按優先級排列 |
| Friction Log | 每15分鐘 | Detect CRM data gaps → ask user to fill |

### SaaS Layer（新增）

| 功能 | 說明 |
|------|------|
| Account Registration | Email+password signup，email verification |
| Tenant Provisioning | 自動 create tenant DB schema + seed default config |
| Team Management | Invite members，3 roles：Admin / Member / Viewer |
| Billing Plans | Free (1 user, basic CRM) / Pro (5 users, AI features) / Enterprise (unlimited, white-label) |
| Integration Hub | Google Calendar OAuth，email sync，CSV import/export |
| Audit Log | 每項 CRM 操作記錄 user + timestamp |
| Data Export | CSV/JSON export per CRM domain |
| White-label | Custom logo + brand color + custom domain |

---

## B — 核心架構原則（G08 Principles）

呢個系統係產品，唔係 scripts collection。以下係所有開發決策嘅底層規則。

### 原則 1：Schedule in PG, Not External Cron
所有排程必須喺 PostgreSQL 入面，唔可以用 crontab / systemd timer / 任何外部 scheduler。

```
┌──────────────────────────────────────────────┐
│  nexus_schedules table (PG)                   │
│  module_id | schedule_type | cron_expr       │
│  | interval_sec | last_run_at | is_active    │
├──────────────────────────────────────────────┤
│  Single daemon process reads this table      │
│  every 60s, dispatches due modules           │
└──────────────────────────────────────────────┘
```

新 tenant onboarding = INSERT seed schedules + start daemon。唔使改 crontab。

### 原則 2：Zero Hardcode
所有 config 喺 PG 入面，唔可以喺 code 入面 hardcode：
- API keys → `.env` only
- 分類 keywords → `nexus_event_rules` table
- Storage backend type → `nexus_storage_backends` table
- Module enable/disable → `nexus_tenant_modules` table

Code 可以 deploy 俾任何人，tenant-specific config 全部喺 DB + .env。

### 原則 3：Multi-Tenant by Design
- 所有 `nexus_*` tables 有 `tenant_id` FK
- 用 PostgreSQL Row-Level Security（RLS）做 data isolation
- 每個 API request 經 JWT 拎 `tenant_id`，DB 自動 filter
- 唔可以做 schema-per-tenant（100 tenants 用 shared schema + RLS 最簡單）

### 原則 4：LLM One-Shot
- Mechanical work（keyword matching, data sync, threshold checks）→ 零 LLM cost
- 每個 entity trigger LLM 最多一次，用 flag 防止重覆
- LLM 只做 judgment + discovery，唔做 mechanical matching

### 原則 5：Silent by Default
- 冇新 data 就出 `[SILENT]`，唔好出「No new cards to process」
- Module output 只有兩種：有用嘅 message 或者 silence

### 原則 6：Backend-Agnostic Storage
CRM write operations 唔可以 hardcode Notion/HubSpot/Salesforce。用 plugin pattern：
```
nexus.storage_plugins/
  ├── __init__.py   (resolver: 讀 backend_type 從 PG)
  ├── notion/       (writer.py, client.py)
  └── salesforce/   (future)
```

換 backend = UPDATE `nexus_storage_backends` + 新 plugin folder。唔改 code。

### 原則 7：Product = Zero Personal Data in Code
- 無 hardcoded user paths (`/home/user/`)
- 無 hardcoded tenant names / emails
- 所有 secrets from `.env`，fail-fast if missing
- Deploy 步驟：`cp -r nexus/` + create `.env` + run seed → done

### 原則 8：Modular with Runtime Toggle
- 每個功能係獨立 module，有 module_id
- Runtime enable/disable 喺 `nexus_tenant_modules` table
- Core modules（pg_sync, cost_guard）always on，feature modules 可 toggle

---

## C — Web Layout Design Guide（for AI Frontend Generation）

### C1. Layout Architecture

```
┌─────────────────────────────────────────────────────────┐
│ HEADER (56px)                                           │
│ [Logo 24px] [Search ⌘K 240px] [Upgrade] [🔔] [Avatar]  │
├──────────┬──────────────────────────────────────────────┤
│ SIDEBAR  │  MAIN CONTENT                                │
│ (240px)  │  ┌─ Breadcrumb ─── [Page Title] ─────────┐   │
│          │  │                                        │   │
│ Dashboard│  │  Content area (scrollable)             │   │
│ Contacts │  │                                        │   │
│ Companies│  │                                        │   │
│ Deals    │  │                                        │   │
│ Tasks    │  │                                        │   │
│ Touchpts │  └────────────────────────────────────────┘   │
│ NameCards│                                              │
│ Reports  │                                              │
│ Settings │                                              │
├──────────┴──────────────────────────────────────────────┤
│ Footer (32px): Last sync time · Active integrations     │
└─────────────────────────────────────────────────────────┘
```

**Breakpoints:**
- Desktop >= 1024px: sidebar full width 240px, max content width 1280px centered
- Tablet 768-1023px: sidebar collapses to 64px icons only
- Mobile < 768px: sidebar hidden, hamburger overlay

### C2. Navigation Sidebar

```
🏠  Dashboard
👥  Contacts
🏢  Companies
📊  Deals
✅  Tasks
📍  Touchpoints
📇  NameCards
📈  Reports
━━━━━━━━━━━━━
⚙️  Settings
👤  Team
🔌  Integrations
💳  Billing
```

- Active tab: left border 3px `#2563eb`, bg `#334155`
- Hover: bg `#334155`
- Sidebar bg: `#1e293b`, text: `#cbd5e1`
- Collapsed tablet: icon only with tooltip

### C3. Color System

```
Primary:        #2563eb (blue-600)
Primary hover:  #1d4ed8 (blue-700)
Primary light:  #dbeafe (blue-100)

Success:        #059669 (emerald-600)
Warning:        #d97706 (amber-600)
Danger:         #dc2626 (red-600)
Info:           #0284c7 (sky-600)

Surface:        #ffffff
Page bg:        #f8fafc (slate-50)
Card bg:        #ffffff
Border:         #e2e8f0 (slate-200)
Border light:   #f1f5f9 (slate-100)

Text primary:   #0f172a (slate-900)
Text secondary: #64748b (slate-500)
Text muted:     #94a3b8 (slate-400)

Sidebar bg:     #1e293b (slate-800)
Sidebar text:   #cbd5e1 (slate-300)
Sidebar hover:  #334155 (slate-700)
Sidebar active: #2563eb (blue-600)

Status:         🟢 #22c55e  🟡 #eab308  🔴 #ef4444  ⚪ #cbd5e1

Table stripe:   #f8fafc every-other-row
Skeleton:       #f1f5f9 pulse animation
```

### C4. Typography

```
Font family: Inter (body), JetBrains Mono (code/data)

Scale:
  H1: 24px / 700 / 1.3    — Page title
  H2: 18px / 600 / 1.4    — Section header
  H3: 15px / 600 / 1.4    — Card title
  Body: 14px / 400 / 1.5  — Default text
  Body sm: 13px / 400 / 1.5
  Caption: 12px / 500 / 1.3
  Data: 14px / 500 / 1    — Table cells, numbers
```

### C5. Component Inventory

#### C5a. Data Table

```
┌──────────────────────────────────────────────────────────────┐
│ [🔍 Search 240px] [Filter ▼] [Columns ▼] [Export ▼]         │
├──────────────────────────────────────────────────────────────┤
│ ☐ │ Name  ▲ │ Company     │ Email       │ Phone   │ Stage │
│ ☐ │ Peter W │ Kinetix     │ p@k.c       │ 9123    │ 🟢 Act │
│ ☐ │ Mary C  │ HCL         │ m@h.c       │ 9456    │ 🟡 Warm│
│ ☐ │ John L  │ ─           │ j@l.c       │ 9789    │ 🔴 Cold│
├──────────────────────────────────────────────────────────────┤
│ 1-10 of 192  < 1 · 2 · 3 ··· 20 >                          │
└──────────────────────────────────────────────────────────────┘
```

- Header row: 44px, sticky top, bg `#f8fafc`
- Data rows: 48px, hover bg `#f8fafc`, selected bg `#eff6ff`
- Checkbox: 16px
- Sort indicator: ▲/▼ on active column header
- Column resizable via drag
- Pagination: center aligned, current page highlighted

#### C5b. Kanban Board（Deals Pipeline）

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Proposal │ │ Negotiate│ │ P.O.     │ │ Delivery │ │ Closed   │ │ Lost     │
│ 3 deals  │ │ 5 deals  │ │ 2 deals  │ │ 4 deals  │ │ 12 deals │ │ 3 deals  │
│ $1.2M    │ │ $2.1M    │ │ $0.8M    │ │ $1.5M    │ │ $9.2M    │ │ $0.3M    │
├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤
│ Card     │ │ Card     │ │ Card     │ │ Card     │ │          │ │          │
│ Company  │ │ Company  │ │ Company  │ │ Company  │ │          │ │          │
│ $500K    │ │ $600K    │ │ $400K    │ │ $350K    │ │          │ │          │
│ ⭐ 85%   │ │ ⭐ 70%   │ │ ⭐ 95%   │ │ ⭐ 90%   │ │          │ │          │
│ Due: 7d  │ │ Due: 14d │ │ Done     │ │ Done     │ │          │ │          │
│ Peter W  │ │ Mary C   │ │ John L   │ │ Cathy C  │ │          │ │          │
├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤
│ + Add    │ │ + Add    │ │          │ │          │ │          │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

- Column min width 260px, horizontal scroll on overflow
- Column header: stage name + deal count + total value
- Cards: 4px radius, 8px padding, shadow-sm, hover shadow-md
- Card content: company, amount, probability, owner, due date
- Drag-and-drop between columns
- "+ Add" button at bottom of each column
- Probability shown as progress bar: `████░░░ 85%`

#### C5c. Activity Timeline

```
[TODAY]
  ─────────────────────────────────────────
  ● 14:30  📞 Call with Peter Wong
           Notes: Discussed Q4 pipeline, demo scheduled
           🔗 Kinetix · Project HKMA
  ─────────────────────────────────────────
  ● 10:00  ✅ Task: Follow up proposal — Completed
  ─────────────────────────────────────────
  ● 09:15  📎 Attachment: proposal_v3.pdf added to Deal

[YESTERDAY]
  ─────────────────────────────────────────
  ● 16:00  📇 NameCard scanned: Cathy Cheung
           Digidations · Director
  ─────────────────────────────────────────
  ● 11:30  🤝 Meeting: Vendor Briefing - HPE
           🏢 HPE Hong Kong · 👥 3 attendees
```

- Vertical line: 2px `#e2e8f0`
- Dots: 12px, coloured by type（📞=blue, ✅=green, 📇=purple, 🤝=orange）
- 24px gap between items
- Sticky section headers: TODAY / YESTERDAY / date
- Click on item → expand detail

#### C5d. Stats Card

```
┌──────────────────────────┐
│ Total Deals              │
│ $4,200,000    ▲ 12%      │
│ 14 active projects       │
└──────────────────────────┘
```

- Grid: 1-4 cards per row (responsive)
- Padding: 20px
- Icon optional top-left
- Trend arrow + percentage colored green/red
- Subtle border + shadow-sm

#### C5e. Dashboard Layout

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│  Stats Card  │  Stats Card  │  Stats Card  │  Stats Card  │
├──────────────┴──────────────┼──────────────┴──────────────┤
│  Tasks (urgent, top 5)      │  Upcoming Events (next 7d)  │
├─────────────────────────────┴─────────────────────────────┤
│  Deal Pipeline (mini kanban, first 3 columns)             │
├─────────────────────────────┬─────────────────────────────┤
│  Recent Activity (last 5)   │  Deals by Stage (pie chart) │
└─────────────────────────────┴─────────────────────────────┘
```

### C6. Page Templates

#### C6a. Login / Signup

```
Centered card 400px on gradient bg #2563eb → #1d4ed8

┌──────────────────────────────────┐
│                                  │
│         [Logo 48px]              │
│        NEXUS CRM                 │
│                                  │
│  ┌────────────────────────────┐  │
│  │ Email                      │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │ Password                   │  │
│  └────────────────────────────┘  │
│                                  │
│  [ ] Remember me  Forgot?       │
│                                  │
│  ┌────────────────────────────┐  │
│  │      Sign In               │  │
│  └────────────────────────────┘  │
│                                  │
│  Don't have an account? Sign up │
└──────────────────────────────────┘
```

- Input: height 44px, border `#cbd5e1`, focus ring 3px `#2563eb`
- Button: height 44px, bg `#2563eb`, hover `#1d4ed8`, text white 700

#### C6b. Settings

```
Two-panel layout:
Left (240px):  nav links
  ── Profile
  ── Team
  ── Integrations
  ── Billing
  ── Preferences

Right: form content

PROFILE:
  [Avatar 128px circle]  [Upload]
  Name:  [________________]
  Email: [________________]  ✓ Verified
  Phone: [________________]
  Timezone: [▼ Asia/Hong_Kong]

TEAM:
  ┌──────────────────────────────────────────────┐
  │ Peter Wong   peter@k.c     Admin    [Remove] │
  │ Mary Chan    mary@k.c      Member   [Remove] │
  │                                  [Invite +] │
  └──────────────────────────────────────────────┘

INTEGRATIONS:
  ┌──────────────────────────────────────────────┐
  │ [Google logo]  Google Calendar               │
  │ ✓ Connected as terry@k.c  [Disconnect]      │
  │ Last sync: 2 minutes ago                     │
  └──────────────────────────────────────────────┘
  ┌──────────────────────────────────────────────┐
  │ [Notion logo]  Notion CRM                    │
  │ ○ Not connected  [Connect]                   │
  └──────────────────────────────────────────────┘
```

#### C6c. NameCard Scanner

```
┌──────────────────────────────────────────────────────────────┐
│ [📸 Upload Card  #2563eb]  or drag & drop images here       │
├──────────────────────────┬───────────────────────────────────┤
│                          │  Extracted Data                   │
│   [Card Preview]         │  ─────────────────────           │
│                          │  Name: Cathy Cheung              │
│    original image        │  Title: Director                  │
│    with corner overlay   │  Company: Digidations HK          │
│                          │  Phone: +852 9123 4567            │
│                          │  Email: cathy@digidations.com     │
│                          │  Address: Unit 123, ...          │
│                          │───────────────────────────────────│
│                          │  [✅ Save to CRM] [🔄 Re-scan]   │
└──────────────────────────┴───────────────────────────────────┘
```

#### C6d. Contact Detail / Company Detail

```
Two-panel layout:
Left (320px): Profile card
  ┌──────────────────────┐
  │  [Avatar 80px]       │
  │  Peter Wong          │
  │  Sales Director      │
  │  Kinetix Systems     │
  │  ──────────────────  │
  │  📞 +852 9123 4567  │
  │  ✉️ peter@k.c       │
  │  📍 Unit X, ...     │
  │  ──────────────────  │
  │  [Edit] [Delete]     │
  └──────────────────────┘

Right: tabbed content
  [Activity] [Deals] [Tasks] [Files]
  
  ACTIVITY TAB: timeline view (same as C5c)
  DEALS TAB: mini kanban cards for this contact
  TASKS TAB: task list filtered by contact
```

#### C6e. Empty States

- **Empty table**: ghost icon 48px + "No contacts yet" + "Import from CSV" CTA button
- **No search results**: "No results for "xxx"" + "Try different keywords"
- **Error state**: red banner at top "Failed to load data" + [Retry] button
- **Loading**: skeleton cards (pulse animation, `#f1f5f9` bg, rounded 4px)

### C7. Interaction Patterns

| Element | Default | Hover | Active/Focus | Disabled |
|---------|---------|-------|-------------|----------|
| Button | bg primary | bg darken 10% | scale 0.97 | opacity 0.5 |
| Input | border #cbd5e1 | — | border #2563eb + ring 3px | bg #f1f5f9 |
| Table row | bg white | bg #f8fafc | selected: bg #eff6ff | — |
| Sidebar item | bg transparent | bg #334155 | left border 3px #2563eb | — |
| Card | shadow-sm | shadow-md | — | — |
| Dropdown | border #e2e8f0 | border #2563eb | — | — |
| Toggle switch | bg #cbd5e1 | — | bg #2563eb | opacity 0.5 |

### C8. Modal / Dialog Pattern

```
┌─────────────────────────────────────────┐
│  [X]  Create New Contact                │
├─────────────────────────────────────────┤
│  First Name    [________________]       │
│  Last Name     [________________]       │
│  Email         [________________]       │
│  Phone         [________________]       │
│  Company       [▼ Select or type... ]   │
│  Job Title     [________________]       │
│                                         │
│  Tags: [Prospect] [VIP] [Partner]       │
│                                         │
│  [Cancel]              [Create]         │
└─────────────────────────────────────────┘
```

- Width: 480px (mobile: fullscreen with 16px padding)
- Overlay: `rgba(0,0,0,0.5)` 40%
- Close: X button + click outside + Escape key
- Form fields: standard input pattern
- Buttons: Cancel (outline) on left, Create (primary) on right

### C9. Notifications / Toast

```
┌──────────────────────────────────────┐
│ ✅ Contact created successfully      │
└──────────────────────────────────────┘
```

- Position: top-right, 16px from edges
- Width: 360px max
- Types: ✅ success (green left border), ⚠️ warning, ❌ error, ℹ️ info
- Auto-dismiss: 4 seconds. Hover to pause.
- Stack vertically, newest on top

### C10. Responsive Rules

- **Desktop** (>= 1024px): sidebar visible, max width 1280px centered
- **Tablet** (768-1023px): sidebar collapsed to 64px icons, content full width
- **Mobile** (< 768px): sidebar hidden (hamburger), content full width, stacked layouts
- **Data tables** on mobile: horizontal scroll with sticky first column (name)
- **Kanban** on mobile: single column, cards stacked vertically
- **Forms** on mobile: full width inputs, no multi-column

---

## D — Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Tailwind CSS + Radix UI |
| State | TanStack Query (server) + Zustand (client) |
| Tables | TanStack Table |
| Forms | React Hook Form + Zod |
| Charts | Recharts |
| Kanban | custom (or @hello-pangea/dnd) |
| Backend | FastAPI (Python 3.12) |
| Auth | JWT + refresh token + httpOnly cookies |
| Database | PostgreSQL 16 with Row-Level Security |
| Queue | PG-based scheduler (same as G08 pattern) |
| File storage | local disk (S3-compatible for scale) |
| Deployment | Docker Compose (single VM, 100 tenants fine) |

---

## E — API Contract（Frontend-Backend）

### Authentication

```
POST  /api/auth/signup       { email, password, company_name }
POST  /api/auth/login        { email, password } → { access_token, refresh_token }
POST  /api/auth/refresh      { refresh_token } → { access_token }
GET   /api/auth/me           → { user, tenant }
```

### CRM CRUD

```
GET    /api/contacts                ?search&company_id&page&limit
GET    /api/contacts/:id            
POST   /api/contacts                { name, email, phone, company_id, ... }
PATCH  /api/contacts/:id            
DELETE /api/contacts/:id            

GET    /api/companies               
GET    /api/companies/:id           
POST   /api/companies               
PATCH  /api/companies/:id           
DELETE /api/companies/:id           

GET    /api/deals                   ?stage&company_id&page
GET    /api/deals/:id               
POST   /api/deals                   
PATCH  /api/deals/:id               
PATCH  /api/deals/:id/stage         { stage }  (move kanban column)

GET    /api/tasks                   ?status&priority&due_date
POST   /api/tasks                   
PATCH  /api/tasks/:id               

GET    /api/touchpoints             ?contact_id&company_id&page
POST   /api/touchpoints             

GET    /api/namecards               ?page
POST   /api/namecards/upload        multipart image
POST   /api/namecards/:id/process   trigger OCR pipeline

GET    /api/dashboard/stats         
GET    /api/dashboard/recent-activity
```

### Settings & Team

```
GET    /api/settings/profile        
PATCH  /api/settings/profile        

GET    /api/team                    
POST   /api/team/invite             { email, role }
DELETE /api/team/:user_id           

GET    /api/integrations            
POST   /api/integrations/google     OAuth flow
DELETE /api/integrations/:id        

GET    /api/billing/plan            
GET    /api/billing/invoices        
```

### WebSocket（Real-time）

```
wss://<host>/ws/dashboard
  → server pushes: new_touchpoint, deal_stage_change, task_update, notification

wss://<host>/ws/notifications
  → server pushes: meeting_nudge, task_due, system_alerts
```

---

## F — Data Model（SaaS Tables Additions）

### New Tables（sao_ prefix — SaaS Operations）

```sql
-- Tenant registry
CREATE TABLE saas_tenants (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    plan        TEXT NOT NULL DEFAULT 'free',  -- free/pro/enterprise
    status      TEXT NOT NULL DEFAULT 'active', -- active/suspended/trial
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    settings    JSONB DEFAULT '{}'  -- white-label config
);

-- Users
CREATE TABLE saas_users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES saas_tenants(id),
    email           TEXT NOT NULL,
    password_hash   TEXT NOT NULL,
    name            TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'member', -- admin/member/viewer
    is_active       BOOLEAN DEFAULT true,
    last_login      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, email)
);

-- Plans
CREATE TABLE saas_plans (
    id          TEXT PRIMARY KEY, -- 'free' / 'pro' / 'enterprise'
    name        TEXT NOT NULL,
    price_month NUMERIC(10,2),
    max_users   INTEGER DEFAULT 1,
    max_storage_mb INTEGER DEFAULT 100,
    features    JSONB NOT NULL DEFAULT '{}' -- { ai_brief: true, namecard: true }
);

-- Billing
CREATE TABLE saas_billing (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES saas_tenants(id),
    plan_id         TEXT NOT NULL REFERENCES saas_plans(id),
    stripe_customer TEXT,
    status          TEXT DEFAULT 'active',
    next_billing    DATE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Integrations (encrypted credentials storage)
CREATE TABLE saas_integrations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL REFERENCES saas_tenants(id),
    provider        TEXT NOT NULL, -- google_calendar / notion / google_drive
    credentials     TEXT,  -- encrypted JSON
    is_active       BOOLEAN DEFAULT false,
    last_sync_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, provider)
);

-- Audit log
CREATE TABLE saas_audit_log (
    id          BIGSERIAL PRIMARY KEY,
    tenant_id   UUID NOT NULL REFERENCES saas_tenants(id),
    user_id     UUID REFERENCES saas_users(id),
    action      TEXT NOT NULL,  -- contact.create / deal.stage_change
    entity_type TEXT,
    entity_id   TEXT,
    details     JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### RLS Policy Example

```sql
-- On nexus_contacts:
ALTER TABLE nexus_contacts ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON nexus_contacts
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- On all nexus_* tables, same pattern
```

---

## G — Frontend Route Map

```
/login                          → Login page
/signup                         → Registration + tenant creation
/reset-password                 → Password reset

/                               → Dashboard (redirect to /dashboard)
/dashboard                      → Stats cards + tasks + pipeline + activity

/contacts                       → Contacts table
/contacts/new                   → Create contact form
/contacts/:id                   → Contact detail (profile + activity + deals)

/companies                      → Companies table
/companies/new                  → Create company
/companies/:id                  → Company detail

/deals                          → Kanban board
/deals/:id                      → Deal detail

/tasks                          → Tasks table
/tasks/new                      → Create task

/touchpoints                    → Activity timeline (all)

/namecards                      → NameCard scanner page
/namecards/:id                  → Single card detail

/reports                        → Reports & analytics

/settings/profile               → User profile
/settings/team                  → Team management
/settings/integrations          → Integration setup (Google, Notion)
/settings/billing               → Plan & billing
/settings/preferences           → Notification preferences, timezone
```

---

*This document is self-contained. AI can generate frontend source code from Section C onwards. Backend developer (Hermes) will implement API endpoints, database schema, and SaaS layer based on Sections A, B, D, E, F.*
