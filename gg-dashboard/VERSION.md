# GG Dashboard v1.0

**Release:** 2026-06-08
**Design influence:** Dribbble healthcare-style (A8D5B5, F4C7A8, D0C8F0)
**Design system:** designlang extraction completed (24 files, ~224K)
**CSS refactor:** -148 lines, container max-width unified to 393px

## Tabs
- Home — system status + reminders + insights
- Intel — AI-generated intelligence feed
- Tasks — Notion Task Center pipeline (Ivy 6 format)
- Servants — three AI role cards + thoughts
- System — overall health + PG sync status

## Data Pipeline
- gg-data.json — refreshed every 15min (cron: hermes_dashboard_sync.py)
- gg-insights.json — AI intelligence collector
- sync_to_pg.py — PG audit trail
- Notion bridge — bidirectional task sync

## Cron Touchpoints (delivered to Telegram)
- 07:30 Morning Briefing (LLM)
- 07:45 Morning Task Digest (LLM, auto-pin, weekdays only)
- 08:15 Devotion (daily, with inline buttons)
- 09:00 Clock-in (no-agent)
- 13:30 Lunch Check-in (LLM)
- 17:30 Commute Preview
- 18:00 Sign-off + Clock-out
- 20:00 Sub Agent Review
- 22:00 Evening Check-in
- 23:00 Nightly Auto Process

## Infra
- Flask on :7870
- Cloudflare tunnel: intel.kinet-poc.com
- designlang MCP available for future cleanup
