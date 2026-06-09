# GG AI Dashboard — Project Context

> 最後更新：2026-06-09
> Status：Production

## Overview

GG Dashboard 係 Terrence 嘅 AI 管家控制台，整合系統監控、任務管理、AI 情報同 Agent 面板。v2.0 已完成 iOS-native 重寫，100% 符合 Apple HIG。

## Versions

- **v1.0** — Baseline Flask dashboard with designlang extraction
- **v1.1** — CSS refactor (−4,090 bytes) + WCAG AA fix
- **v1.2** — Apple HIG compliance + iPhone 14 Pro guideline (14 fixes)
- **v2.0** — Full iOS-native rewrite (Apple HIG 100% compliance)

## Infrastructure

| Component | Detail |
|-----------|--------|
| Backend | Flask on :7870 |
| Auth | Cloudflare Access |
| Tunnel | Cloudflare: intel.kinet-poc.com |
| Data refresh | Every 15min (cron) |
| Notion sync | Bidirectional task sync |

## Key Endpoints

- `/` — Home (system status, reminders, insights)
- `/intel` — AI intelligence feed
- `/tasks` — Notion Task Center pipeline
- `/agents` — AI role cards
- `/profile` — System profile
