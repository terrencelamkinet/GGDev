# G08 NEXUS CRM v2 — Project Context

| 最後更新：2026-07-09 00:45 HKT
| 由 GG Fighter 於 G08 NEXUS CRM tasks/projects enrichment session 更新

---

## 1. 專案定位

NEXUS CRM v2 係一個 AI-powered CRM intelligence layer，wraps around 現有 GG infrastructure（Notion CRM + Task Hub PG + Google Calendar），提供 intelligent meeting prep、CRM enrichment、relationship health tracking。

**唔係 replacement** — 係 intelligence layer。Read from Notion，enrich in PG，push briefings before meetings。

**Productizable target：** IT Solution Sales teams（starting with Terrence）

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3 — ACTION (LLM)                                      │
│  C3 Meeting Brief · C5 Post-Logger · C8 Rel Coach           │
│  C6 Deal Radar · C7 CRM Daily · C9 Clarification Delivery   │
└─────────────────────────────────────────────────────────────┘
                           │ reads nexus_* tables
┌─────────────────────────────────────────────────────────────┐
│  Layer 2 — INTELLIGENCE (no_agent + LLM on demand)          │
│  C1 Collector (sync + classify + entity match + task enrich)│
│  C4 Health Scorer · Follow-up Radar                         │
└─────────────────────────────────────────────────────────────┘
                           │ PG-First
┌─────────────────────────────────────────────────────────────┐
│  Layer 1 — DATA (PG nexus_* tables, 18 tables)              │
│  Notion → PG sync via Central CRM Sync (30min)              │
│  + Existing `tasks` table (Task Hub, separate concern)      │
└─────────────────────────────────────────────────────────────┘
                           │ reads
┌─────────────────────────────────────────────────────────────┐
│  Layer 0 — EXISTING INFRASTRUCTURE                           │
│  PostgreSQL task_hub @ 127.0.0.1:5432                       │
│  Notion CRM (7 DBs) · Google Calendar · schedule_data.json  │
│  74 existing cron jobs (untouched)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. PG Schema（18 nexus_* tables）

| Table | Purpose | Populated |
|-------|---------|:---------:|
| `nexus_tenants` | Multi-tenant config | ✅ 1 row |
| `nexus_modules` | Module registry (29 modules) | ✅ |
| `nexus_tenant_modules` | Per-tenant toggle | ✅ |
| `nexus_module_config` | Per-module params | ✅ |
| `nexus_storage_backends` | Notion DB IDs | ✅ 7 domains |
| `nexus_locations` | Venue classification | ✅ 3 locations |
| `nexus_event_rules` | 14-type classification | ✅ 12 rules |
| `nexus_events` | Classified events + CRM context | ✅ |
| `nexus_companies` | Company cache | ✅ 96 |
| `nexus_contacts` | Contact cache | ✅ 190 |
| `nexus_projects` | Project cache | ✅ 57 |
| `nexus_touchpoints` | Touchpoint cache | ✅ 21 |
| `nexus_tasks` | **CRM tasks from Notion Task Center** | ✅ 112 |
| `nexus_products` | Product cache | ✅ 84 |
| `nexus_brands` | **Brand cache** | ✅ 86 |
| `nexus_ai_cache` | AI analysis dedup | ✅ |
| `nexus_sync_state` | Sync health tracker | ✅ 8 domains healthy |
| `nexus_clarifications` | Data gap Q&A | ✅ |
| `nexus_clarification_rules` | Clarification triggers | ✅ |
| `nexus_clarification_silence` | Per-event silence | ✅ |

**Existing tables reused (not NEXUS-owned):**
- `tasks` — Task Hub internal operations (notion_task_sync.py → tasks table)
- `commute_state`, `location_log` — Commute system

---

## 4. Cron Jobs（10 NEXUS + 74 existing = 84 total）

| ID | Name | Schedule | Type | Script | Deliver | Status |
|----|------|----------|------|--------|:-------:|:------:|
| C1 | NEXUS Collector | */15 | no_agent | `nexus_c1_collector.sh` → `collector.py` | origin | ✅ |
| C2 | NEXUS Nudge | */15 | no_agent | `nexus_c2_nudge.sh` → `nudge.py` | origin | ⚠️ error→fixed |
| C3 | NEXUS Meeting Brief | */15 | **no_agent** ✅ refactored | `nexus_c3_meeting_brief.sh` → `meeting_brief_noagent.py` | origin | ✅ cost saved ~$0.80/day |
| C4 | NEXUS Health Scorer | 04:00 daily | no_agent | `nexus_c4_health_scorer.sh` | origin | ⏳ first run |
| C5 | NEXUS Post-Logger | */15 | no_agent | `nexus_c5_post_logger.sh` | origin | ✅ |
| C6 | NEXUS Deal Radar | 08:35 daily | no_agent | `nexus_c6_deal_radar.sh` | origin | ✅ task-aware |
| C7 | NEXUS CRM Daily | 07:32 workdays | no_agent | `nexus_c7_crm_daily.sh` | origin | ✅ task-aware |
| C8 | NEXUS Rel Coach | Mon 09:05 | no_agent | `nexus_c8_rel_coach.sh` | origin | ⏳ first run |
| C9 | NEXUS Clarification | */15 | no_agent | `nexus_c9_clarification_delivery.sh` | origin | ✅ |
| — | Central CRM Sync | */30 | no_agent | `nexus_notion_crm_sync.sh` | local | ✅ 646 entities |
| — | Cron Registry | */30 | no_agent | `nexus_cron_registry.sh` | local | ✅ |
| — | Aug 1 cleanup | once 2026-08-01 | LLM | removes old deprecated crons | origin | 🗓️ |

**Deprecated (paused, auto-remove Aug 1):**
- `c2859531eaf5` — event_pre_notify.py
- `92cb185d46de` — LLM meeting prep (old)

---

## 5. Key File Paths

| Path | Purpose |
|------|---------|
| `/home/airoot/.hermes/nexus/` | NEXUS project root |
| `/home/airoot/.hermes/nexus/core/config.py` | Config reader (sync psycopg2) |
| `/home/airoot/.hermes/nexus/core/pg.py` | PG connection helper |
| `/home/airoot/.hermes/nexus/core/module_registry.py` | Module toggle |
| `/home/airoot/.hermes/nexus/core/cost_guard.py` | LLM budget |
| `/home/airoot/.hermes/nexus/modules/collector.py` | C1: sync + classify + match + task enrich |
| `/home/airoot/.hermes/nexus/modules/notion_crm_sync.py` | Central CRM Sync (7 domains) |
| `/home/airoot/.hermes/nexus/modules/schedule/nudge.py` | C2: pre-event nudge |
| `/home/airoot/.hermes/nexus/modules/intelligence/meeting_brief.py` | C3 context builder |
| `/home/airoot/.hermes/nexus/modules/intelligence/post_logger.py` | C5: post-meeting logger |
| `/home/airoot/.hermes/nexus/modules/intelligence/deal_radar.py` | C6: deal risk radar |
| `/home/airoot/.hermes/nexus/modules/intelligence/crm_daily.py` | C7: daily CRM briefing |
| `/home/airoot/.hermes/nexus/modules/intelligence/rel_coach.py` | C8: relationship coach |
| `/home/airoot/.hermes/nexus/modules/intelligence/clarification.py` | C9: clarification engine |
| `/home/airoot/.hermes/nexus/modules/crm/health_scorer.py` | C4: health scoring |
| `/home/airoot/.hermes/nexus/modules/crm/entity_matcher.py` | CRM→event matching |
| `/home/airoot/.hermes/nexus/storage_plugins/notion/client.py` | Notion read client |
| `/home/airoot/.hermes/nexus/storage_plugins/notion/writer.py` | Notion write-back |
| `/home/airoot/.hermes/nexus/storage_plugins/notion/quirks.py` | Notion quirks centralised |
| `/home/airoot/.hermes/nexus/migrations/005_tasks_and_brands.sql` | Latest migration |
| `/home/airoot/.hermes/nexus/G08-PLAN.md` | Project plan |
| `/home/airoot/.hermes/nexus/CORE-PRINCIPLES.md` | 11 core principles |
| `/home/airoot/.hermes/scripts/nexus_c*_*.sh` | Cron wrapper scripts (7 files) |
| `/home/airoot/.hermes/nexus_cron_registry.json` | Cron definitions for AI preview |
| `/home/airoot/.hermes/nexus/delivery/` | Delivery modules |
| `/home/airoot/.hermes/nexus/seeds/terrence_seed.sql` | Seed data |

---

## 6. Design Principles（應用中）

1. **Strangler Fig** — Shadow → Validate → Cutover ✅ Done
2. ~~【測試版】Prefix~~ — No longer needed (cutover complete)
3. **零影響** — 唔郁 existing cron / tables ✅
4. **Zero Hardcode** — Config in PG, not code ✅
5. **Multi-Tenant** — tenant_id on all tables ✅
6. **CISP** — .env only, read-only Notion, rollback plan ✅
7. **模組化** — 29 modules, runtime toggle ✅
8. **Silent by Default** — no_agent scripts output [SILENT] when idle ✅
9. **PG-First, Notion-Second** — Data to PG first, then Notion ✅
10. **Cutover Protocol** — Pause old → enable new, rollback <1min ✅
11. **Centralize First** — Central CRM Sync, not per-domain syncs ✅

---

## 7. Pending Work

### 🟡 A: Name Card OCR Module
**Why:** 現有 `namecard_scanner.py` 係獨立 script，唔係 NEXUS module。
**What:**
- [ ] 建立 `nexus/modules/crm/namecard.py`
- [ ] Step 1: OCR（SiliconFlow vision API / tesseract）
- [ ] Step 2: Entity match（company→nexus_companies, name→nexus_contacts）
- [ ] Step 3: Create/update nexus_contacts + Notion CRM
- [ ] Step 4: Log touchpoint「名卡交換」
- [ ] 註冊為 NEXUS module（crm.namecard）
- [ ] 整合入 Central CRM Sync 排程（唔另開 cron）

### 📌 Completed This Session (2026-07-09)
- ✅ **C3 → no_agent**: 由 LLM cron 改做 no_agent script。每日 cost 由 ~$0.80 → ~$0.02
- ✅ **C6 Deal Radar**: + overdue tasks + tasks due within 14 days per project
- ✅ **C7 CRM Daily**: + open tasks summary + due-this-week + overdue tasks sections

### ⚠️ Known Issues（要 fix）
- [ ] C1/C2 之前「Script not found」error — 已整 wrappers，聽朝 verify
- [ ] C5 Post-Logger 曾有 error — 手動 run 正常，聽朝 confirm cron log
- [ ] Entity matcher 未 populate crm_project_ids → task enrichment 未有 output
- [ ] 2 old crons paused but not deleted（Aug 1 auto-remove queued）

### 🔮 Future（觀察後決定）
- [ ] NEXUS Dashboard（Web UI）
- [ ] Analytics（deal velocity, trends）
- [ ] Multi-tenant（second client）
- [ ] CISP audit log

---

## 8. Cost Tracking（每日 cap $1.50 USD）

| Module | LLM? | Est daily cost |
|--------|:----:|:--------------:|
| C1 Collector | ❌ | $0 |
| C2 Nudge | ❌ | $0 |
| C3 Meeting Brief | ⚠️**要refactor** | ~$0.80（*/15 ticks） |
| C4 Health Scorer | ❌ | $0 |
| C5 Post-Logger | ❌ | $0 |
| C6 Deal Radar | ✅ | ~$0.05 |
| C7 CRM Daily | ✅ | ~$0.10 |
| C8 Rel Coach | ✅ | ~$0.05/wk |
| C9 Clarification | ❌ | $0 |
| Central CRM Sync | ❌ | $0 |
| **Total** | | **~$1.00/day** (after refactor: ~$0.20/day) |

---

## 9. Session History Reference

**2026-07-08 重要事件：**
- 15:00 — Start G08 NEXUS CRM v2 build
- 18:52 — Phase 1-3 deployed, shadow mode
- 20:00 — C9 clarification tested → user replied with Systex contact names
- 22:00 — Cutover: all NEXUS crons → deliver:origin
- 22:30 — Fix script path bug (wrapper scripts)
- 22:48 — Cron Registry created
- 22:50 — Today's meeting touchpoints checked (3 meetings, 1 TP created, 2 skipped)
- 23:00 — **Migration 005**: nexus_tasks + nexus_brands added
- 23:10 — Central CRM Sync: 646 entities across 7 domains healthy
- 23:15 — CONTEXT.md created
