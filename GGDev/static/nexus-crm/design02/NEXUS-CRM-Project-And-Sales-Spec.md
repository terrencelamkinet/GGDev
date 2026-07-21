***REMOVED*** NEXUS CRM — Project & Sales Module Spec

For AI to build Project Details page + Sales module into design02 (Ivory Edition).

---

***REMOVED******REMOVED*** 1. New Entity: Project

***REMOVED******REMOVED******REMOVED*** 1.1 Field List

| Field | Type | Notes |
|-------|------|-------|
| id | auto int | primary key |
| name | text | project name |
| description | textarea | long text |
| status | enum | `planning`, `in_progress`, `on_hold`, `completed`, `cancelled` |
| priority | enum | `p0` (critical), `p1` (high), `p2` (medium), `p3` (low) |
| company_id | int | FK → companies |
| customer_id | int | FK → contacts (primary stakeholder) |
| start_date | date | YYYY-MM-DD |
| target_end | date | YYYY-MM-DD |
| actual_end | date | nullable |
| budget | string | e.g. "$120,000" |
| spent | string | e.g. "$85,000" — auto-calc from related tasks/deals? |
| stage | enum | `kickoff`, `discovery`, `execution`, `uat`, `handover`, `closed` |
| deal_id | int | nullable, FK → deals (linked opportunity) |
| owner_id | int | FK → team_members (see Sales module) |
| tags | string[] | e.g. ["infra", "migration", "security"] |
| notes | text | internal notes |
| created_at | date | auto |
| updated_at | date | auto |

***REMOVED******REMOVED******REMOVED*** 1.2 Sample Data

```javascript
projects: [
  {
    id: 1,
    name: 'Vantage Storage Refresh Q3',
    description: 'Replace legacy SAN with NetApp ASA A-Series across 3 data centres.',
    status: 'in_progress',
    priority: 'p1',
    company_id: 1,  // Vantage Holdings
    customer_id: 1, // Ada Cheung
    start_date: '2026-06-15',
    target_end: '2026-09-30',
    budget: '$482,000',
    spent: '$210,000',
    stage: 'execution',
    deal_id: 1,     // Storage Refresh Q3 deal
    owner_id: 1,    // TL
    tags: ['storage', 'netapp', 'infra'],
    notes: 'Client requested phased rollout — Phase 1 by Aug 15.'
  },
  {
    id: 2,
    name: 'Harbour Tech DR Site Migration',
    description: 'Disaster recovery site setup at HKT data centre.',
    status: 'planning',
    priority: 'p2',
    company_id: 3,
    customer_id: 3, // Elaine Kwok
    start_date: '2026-08-01',
    target_end: '2026-12-31',
    stage: 'kickoff',
    deal_id: 2,
    owner_id: 1,
    tags: ['dr', 'migration', 'datacentre']
  }
]
```

***REMOVED******REMOVED******REMOVED*** 1.3 Relationships

```
Project ──belongs_to──> Company
Project ──has_one──────> Contact (customer/primary stakeholder)
Project ──has_many─────> Task (filtered by project_id)
Project ──belongs_to──> Deal (linked opportunity, optional)
Project ──belongs_to──> TeamMember (owner)
```

***REMOVED******REMOVED******REMOVED*** 1.4 API Contract (GET / POST / PUT)

```
GET /api/projects          → { projects: Project[] }
GET /api/projects/:id      → { project: Project, tasks: Task[], touchpoints: Touchpoint[] }
POST /api/projects         → body: Project (without id)
PUT /api/projects/:id      → body: partial Project
DELETE /api/projects/:id   → { ok: true }
```

***REMOVED******REMOVED******REMOVED*** 1.5 Project Detail Page UI Sections

| Section | Content |
|---------|---------|
| Header | Name, status badge, priority badge, stage |
| Info panel | Budget vs spent progress bar, owner, dates (start→target→actual) |
| Company card | Linked company name + industry (clickable → company-detail) |
| Customer card | Primary contact name, email, phone (clickable → contact-detail) |
| Tasks list | Filtered tasks with priority, status, due date |
| Touchpoints timeline | Filtered by project (same component as existing) |
| Related deal | Linked deal card (if any) |
| Notes | Rich text / textarea |

---

***REMOVED******REMOVED*** 2. Sales Module — Team Management

***REMOVED******REMOVED******REMOVED*** 2.1 New Entity: TeamMember

| Field | Type | Notes |
|-------|------|-------|
| id | auto int | |
| name | text | |
| email | text | |
| phone | text | |
| role | enum | `sales_rep`, `sales_manager`, `director`, `admin` |
| avatar | text | initials fallback, same as existing `initials()` |
| status | enum | `active`, `inactive`, `on_leave` |
| manager_id | int | nullable, FK → team_members (self-ref) |
| territory | text | e.g. "HK Island", "Kowloon East" |
| hire_date | date | |
| quota_monthly | string | e.g. "$200,000" |
| quota_quarterly | string | e.g. "$600,000" |
| quota_yearly | string | e.g. "$2,400,000" |
| personal_notes | text | |

***REMOVED******REMOVED******REMOVED*** 2.2 New Entity: SalesTarget

| Field | Type | Notes |
|-------|------|-------|
| id | auto int | |
| member_id | int | FK → team_members |
| period | string | e.g. "2026-Q3", "2026-07" |
| quota | string | assigned quota |
| achieved | string | actual achieved (auto-calc from closed deals) |
| pipeline | string | total pipeline (auto-calc from open deals) |
| closed_deals | int | count |
| avg_deal_size | string | auto-calc |

***REMOVED******REMOVED******REMOVED*** 2.3 Relations

```
TeamMember ──has_many──> Deal (via owner field)
TeamMember ──has_many──> Project (via owner_id)
TeamMember ──has_many──> SalesTarget
TeamMember ──belongs_to──> TeamMember (manager, self-ref)
```

***REMOVED******REMOVED******REMOVED*** 2.4 Sample Data

```javascript
team: [
  { id: 1, name: 'Terrence Lam', email: 'terrence.lam@terrencepro.hk', role: 'director', manager_id: null, territory: 'HK All', quota_monthly: '$500,000' },
  { id: 2, name: 'Ada Cheung', email: 'ada.cheung@vantageco.com', role: 'sales_rep', manager_id: 1, territory: 'HK Island', quota_monthly: '$200,000' },
  { id: 3, name: 'Marcus Yip', email: 'marcus.yip@brightpeak.io', role: 'sales_rep', manager_id: 1, territory: 'Kowloon East', quota_monthly: '$200,000' },
],
sales_targets: [
  { id: 1, member_id: 1, period: '2026-Q3', quota: '$1,500,000', achieved: '$675,000', pipeline: '$978,000', closed_deals: 1, avg_deal_size: '$675,000' },
  { id: 2, member_id: 2, period: '2026-Q3', quota: '$600,000', achieved: '$96,500', pipeline: '$340,000', closed_deals: 0, avg_deal_size: '—' },
  { id: 3, member_id: 3, period: '2026-Q3', quota: '$600,000', achieved: '$128,000', pipeline: '$128,000', closed_deals: 1, avg_deal_size: '$128,000' },
]
```

***REMOVED******REMOVED******REMOVED*** 2.5 Sales Module Pages

***REMOVED******REMOVED******REMOVED******REMOVED*** 2.5.1 Team List (table)

Columns: Name, Role, Territory, Monthly Quota, Achieved%, Manager, Status
Filters: Role, Territory, Status

***REMOVED******REMOVED******REMOVED******REMOVED*** 2.5.2 Team Member Detail

Sections:
- Profile card: avatar, name, role, contact info, manager
- Quota card: monthly / quarterly / yearly targets vs achieved (visual bar)
- Pipeline: linked deals (kanban filtered by owner)
- Projects: linked projects (table filtered by owner)
- Touchpoints: timeline filtered by member name

***REMOVED******REMOVED******REMOVED******REMOVED*** 2.5.3 Sales Dashboard (new page)

Cards:
- **Team performance**: ranking table (who's closest to quota)
- **Pipeline health**: total pipeline value, avg deal size, win rate %
- **Territory breakdown**: deals by territory
- **Team activity**: recent touchpoints across all team members

***REMOVED******REMOVED******REMOVED*** 2.6 Additional Deals Fields

Add to existing Deal entity (in `D.deals`):

```javascript
// Extended deal fields (add to each deal object)
{
  // ...existing: name, company, amt, prob, owner, due
  project_id: null,       // FK → projects (optional)
  customer_id: 1,         // FK → contacts (primary contact)
  stage: 'proposal',      // same as kanban key
  close_date: '2026-08-04',
  type: 'new_business',   // enum: new_business, renewal, upsell, expansion
  source: 'referral',     // enum: referral, inbound, outbound, partner
  notes: 'Client needs approval from CFO before PO.'
}
```

***REMOVED******REMOVED******REMOVED*** 2.7 API Contract (Sales)

```
GET /api/team              → { team: TeamMember[] }
GET /api/team/:id          → { member: TeamMember, targets: SalesTarget[], deals: Deal[], touchpoints: Touchpoint[] }
POST /api/team             → body: TeamMember (without id)
PUT /api/team/:id          → body: partial TeamMember

GET /api/sales/targets     → { targets: SalesTarget[] }
GET /api/sales/dashboard   → { ranking, pipeline_total, win_rate, territory_breakdown }
```

---

***REMOVED******REMOVED*** 3. Integration: How Projects Connect Everything

```
                      ┌─────────────┐
                      │   Company   │
                      └──────┬──────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼──────┐  ┌───▼───┐  ┌───────▼───────┐
       │   Contact   │  │Project│  │     Deal      │
       │ (Customer)  │  │       │  │ (Opportunity) │
       └──────┬──────┘  └───┬───┘  └───────┬───────┘
              │              │              │
              └──────┬───────┴──────┬───────┘
                     │              │
              ┌──────▼──────┐ ┌─────▼──────┐
              │    Task     │ │ Touchpoint │
              └─────────────┘ └────────────┘

              ┌──────────────┐
              │  TeamMember  │◄── owns Project, Deal
              │ (Sales Rep)  │
              └──────────────┘
```

---

***REMOVED******REMOVED*** 4. Implementation Notes for AI

1. **Add to existing `D` object** — insert `projects`, `team`, `sales_targets` alongside existing `contacts`, `companies`, `deals`, `tasks`, `touchpoints`
2. **Hash routing** — add `projects`, `project-detail/:id`, `team`, `team-detail/:id`, `sales-dashboard` to `pages` object
3. **Sidebar nav** — add Projects (folder icon), Team (users icon), Sales Dashboard (chart icon)
4. **Reuse existing components** — `avatar-sm`, `badge`, `timeline`, `data-table`, `search-box`, `filter-chip`
5. **Colors follow existing CSS variables** — `--color-primary`, `--color-success`, `--color-warning`, `--color-text`, etc.
6. **All new pages follow same layout pattern** — breadcrumb → page-header → panel/content
7. **Use same `statusBadge()`, `prioBadge()`, `initials()` helpers** — already defined
8. **Forms** — use existing `.form-row` + `input` / `select` / `textarea` styles from Settings page
