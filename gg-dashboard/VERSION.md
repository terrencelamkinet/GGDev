# GG Dashboard v1.1

**Release:** 2026-06-08  
**Previous:** v1.0 (designlang extraction baseline + initial CSS cleanup)  
**Design influence:** Dribbble healthcare-style (A8D5B5, F4C7A8, D0C8F0)  
**Design system:** designlang extraction v2 (fresh analysis against actual templates)  
**CSS refactor:** -4,090 bytes, from 5,718 → 1,628 (71% reduction), duplicate declarations eliminated  
**a11y fix:** time-label contrast 1.67:1 → 5.9:1 (AA pass)

## v1.1 Changes
- Removed all unused CSS classes (badge, header, greeting, metric-card, card, tag, nav-tab, col2, etc.)
- Preserved only: CSS variables, resets, .container, .time-label, @keyframes fadeUp, responsive + dark mode
- Fixed WCAG AA contrast fail on time-label (was #b2bec3 on #f0f0f5)
- designlang v1.1 extraction output: `/home/airoot/design-extract-v1.1/` (fresh)

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
