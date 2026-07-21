# NEXUS CRM — SaaS Platform Build Guide

> 以下係 AI frontend developer 需要知道嘅所有 specification。UI/UX design 自由創作，呢份嘢只講功能、頁面、同 API contract。

---

## 1. Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Tailwind CSS |
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 |
| Auth | JWT + refresh token |

---

## 2. Pages List

### 2.1 Login Page `/login`
- Email + password form
- Link to signup
- "Forgot password" link
- On success: store JWT, redirect to /dashboard

### 2.2 Signup Page `/signup`
- Name, email, password, company name fields
- On submit: POST /api/auth/signup → auto-login → redirect to /dashboard/welcome
- Welcome screen: "Connect your Google Calendar" or "Skip for now"

### 2.3 Dashboard `/dashboard`
4 stat cards at top:
- Total Contacts, Active Deals ($ total), Open Tasks, Upcoming Events (next 7 days)

Below stat cards, 3 panels:
1. **Recent Activity** — last 5 touchpoints/events, time-sorted (activity feed style)
2. **Upcoming Events** — next 5 calendar events with time, title, company
3. **Tasks Due Soon** — top 5 tasks due within 7 days, with priority badge

Bottom section:
- **Deal Pipeline** — mini kanban showing first 3 stages (Proposal / Negotiate / PO), max 3 cards each

### 2.4 Contacts Page `/contacts`
- **Table view** with columns: Name, Email, Phone, Company, Last Touchpoint date, Status (Active/Warm/Cold)
- Search bar (search by name, email, company)
- Click row → `/contacts/:id` detail page
- +New Contact button opens modal form

**Contact Detail `/contacts/:id`**
Left panel: profile card (avatar, name, title, company, email, phone, address, tags)
Right panel: tabbed view
- Tab "Activity": timeline of all touchpoints/meetings with this contact
- Tab "Deals": list of deals linked to this contact
- Tab "Tasks": list of tasks linked to this contact

### 2.5 Companies Page `/companies`
- **Table view** with columns: Name, Industry, Contacts count, Active Deals, Status
- Search bar + industry filter dropdown
- Click row → `/companies/:id`

**Company Detail `/companies/:id`**
- Company info card (name, industry, phone, address, website)
- Contacts section: list of people from this company (inline mini-table)
- Deals section: list of deals from this company
- Touchpoint section: recent activity with this company

### 2.6 Deals Page `/deals`
- **Kanban board view** with 6 columns: Proposal, Negotiate, P.O., Delivery, Closed Won, Lost
- Each card shows: deal name, company, amount, probability %, owner name, due date (if any)
- Drag-and-drop between columns to change stage
- +New Deal button opens modal

**Deal Detail `/deals/:id`**
- Deal info (name, amount, probability, stage, company link, owner, close date, notes)
- Activity timeline for this deal

### 2.7 Tasks Page `/tasks`
- **Table view**: Title, Priority (P0 🔴 / P1 🟡 / P2 🔵 / P3 ⚪), Status, Due date, Related Deal
- Filter by priority, status, date range
- +New Task modal

### 2.8 Touchpoints Page `/touchpoints`
- **Activity timeline view** (vertical timeline)
- Each entry shows: type icon (📞 call, 🤝 meeting, ✉️ email, 📇 namecard), title, date, related company/contact
- Filter by contact, company, date range

### 2.9 NameCards Page `/namecards`
- Grid of uploaded namecard images + extracted data side by side
- Upload button → opens file picker
- Each card: image thumbnail + extracted fields (name, title, company, phone, email)
- [Save to CRM] button → create contact
- [Re-scan] → re-run OCR

### 2.10 Settings Page `/settings`

**Profile** tab: edit name, email, phone, avatar, timezone

**Team** tab: table of team members (name, email, role, status)
- Invite button → send invite email
- Remove member (admin only)

**Integrations** tab:
- Google Calendar: connect/disconnect button, show status
- (Future: Notion, Slack, etc.)

**Billing** tab: current plan, upgrade/downgrade, invoice history

---

## 3. API Contract

### Auth

```
POST /api/auth/signup
  Body: { name: string, email: string, password: string, company_name: string }
  Response: { access_token, refresh_token, user: { id, name, email }, tenant: { id, name } }

POST /api/auth/login
  Body: { email: string, password: string }
  Response: { access_token, refresh_token, user, tenant }

POST /api/auth/refresh
  Body: { refresh_token }
  Response: { access_token }

GET /api/auth/me
  Header: Authorization: Bearer <token>
  Response: { user, tenant }
```

### Contacts

```
GET  /api/contacts?search=&company_id=&status=&page=1&limit=20
     Response: { items: Contact[], total: number, page: number }

GET  /api/contacts/:id
     Response: Contact (with linked deals, touchpoints, tasks)

POST /api/contacts
     Body: { name, email?, phone?, company_id?, job_title?, address?, tags? }
     Response: Contact

PATCH /api/contacts/:id
     Body: partial Contact fields
     Response: Contact

DELETE /api/contacts/:id
     Response: { ok: true }
```

Contact object:
```
{ id, name, email, phone, company_id, company_name, job_title, 
  address, tags, status, last_touchpoint_at, created_at }
```

### Companies

```
GET  /api/companies?search=&industry=&page=1&limit=20
GET  /api/companies/:id
POST /api/companies (name, industry?, phone?, address?, website?)
PATCH /api/companies/:id
DELETE /api/companies/:id
```

Company object:
```
{ id, name, industry, phone, address, website, contacts_count, 
  active_deals_count, total_deal_value, created_at }
```

### Deals

```
GET  /api/deals?stage=&company_id=&page=1&limit=20
GET  /api/deals/:id
POST /api/deals (name, company_id, amount?, probability?, stage?, owner?, close_date?, notes?)
PATCH /api/deals/:id
PATCH /api/deals/:id/stage  Body: { stage } — for kanban drag
DELETE /api/deals/:id
```

Deal object:
```
{ id, name, company_id, company_name, amount, probability, stage, 
  owner_name, close_date, notes, contact_ids, created_at }
```

Stages: `proposal` | `negotiate` | `po` | `delivery` | `closed_won` | `lost`

### Tasks

```
GET  /api/tasks?status=&priority=&due_before=&page=1&limit=20
GET  /api/tasks/:id
POST /api/tasks (title, priority?, status?, due_date?, deal_id?, assignee_id?)
PATCH /api/tasks/:id
DELETE /api/tasks/:id
```

Task object:
```
{ id, title, priority, status, due_date, deal_id, deal_name, 
  assignee_name, created_at }
```

Priorities: `p0` | `p1` | `p2` | `p3`
Statuses: `pending` | `in_progress` | `done`

### Touchpoints

```
GET  /api/touchpoints?contact_id=&company_id=&page=1&limit=20
POST /api/touchpoints (title, type, contact_id?, company_id?, deal_id?, notes?, date?)
```

Touchpoint object:
```
{ id, title, type, contact_id, contact_name, company_id, company_name,
  deal_id, notes, date, created_at }
```

Types: `meeting` | `call` | `email` | `namecard` | `workshop` | `other`

### NameCards

```
GET  /api/namecards?page=1&limit=20
POST /api/namecards/upload (multipart: image file)
     Response: { id, image_url, status: "pending" }

POST /api/namecards/:id/process
     → triggers OCR pipeline
     Response: { status: "processing" }

GET  /api/namecards/:id
     Response: { id, image_url, extracted: { name, title, company, phone, email, address }, status }

POST /api/namecards/:id/save
     → creates contact from extracted data
     Response: { contact_id }
```

### Dashboard

```
GET /api/dashboard/stats
  Response: { total_contacts, total_deals_value, active_deals_count, 
              open_tasks_count, upcoming_events_count }

GET /api/dashboard/recent-activity?limit=5
  Response: { items: { type, title, description, date, link }[] }

GET /api/dashboard/upcoming-events?days=7
  Response: { items: { title, datetime, company_name }[] }

GET /api/dashboard/tasks-due?days=7
  Response: { items: Task[] }

GET /api/dashboard/deal-pipeline
  Response: { stages: { name, deals: Deal[] }[] }
```

### Team

```
GET  /api/team
     Response: { members: { id, name, email, role, status }[] }

POST /api/team/invite
     Body: { email, role }
     Response: { ok: true }

DELETE /api/team/:user_id
     Response: { ok: true }
```

Roles: `admin` | `member` | `viewer`

### Settings

```
GET  /api/settings/profile
     Response: { name, email, phone, timezone, avatar_url }

PATCH /api/settings/profile
     Body: partial fields
     Response: updated profile

GET  /api/integrations
     Response: { providers: { id, provider, is_active, last_sync_at }[] }
```

---

## 4. Auth Flow (Frontend)

1. On app load: check localStorage for `access_token`
2. If token exists: call `GET /api/auth/me` to validate
3. If valid: store user + tenant in context, show dashboard
4. If invalid/expired: try `POST /api/auth/refresh` with refresh_token
5. If refresh fails: redirect to `/login`

Every API call includes header:
```
Authorization: Bearer <access_token>
```

---

## 5. Data Display Rules

- All monetary values: format as `$1,234,567`
- All dates: show in user's timezone, format `2026-07-21` or `Jul 21, 2026`
- Relative time: "2小時前", "昨日", "3日前"
- Empty states: show ghost icon + descriptive text + CTA button
- Loading: show skeleton pulse animation (not spinner)
- Lists: pagination at bottom (page 1 of 5), 20 items per page default
- No pipe tables in UI — use proper data table components
- Language: English UI, but dates/relative time can be localized

---

## 6. No-Go Rules

- No hardcoded demo data in the frontend code
- No mock API responses in production build (use msw or similar only in dev)
- Don't build billing/payment integration — just UI for plan display
- Don't build real-time WebSocket for v1 — polling is fine
- UI/UX is yours to design — colors, layout, animations are all up to you
- Must be mobile-responsive (sidebar collapses, tables scroll horizontally)
- Must handle loading, empty, and error states for every data view
