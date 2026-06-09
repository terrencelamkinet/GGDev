# G08 — Smart Hub 🧠

**統一 MCP 管家指令中心** — 用一個 command 搞掂每日 briefing、通勤、天氣、系統狀態。

## Overview

將 10 個 MCP servers 整合為一個 unified wrapper layer，用 `gg-commute` 做旗艦功能。朝早自動 push Telegram briefing，支援 cron 自動化同將來 native MCP tool injection。

## Features

| 功能 | 狀態 | 技術 |
|:-----|:----:|:-----|
| `gg-commute` — 通勤 briefing | ✅ | Python wrapper → 4 MCP servers (weather + hkgov + MTR + traffic) |
| Telegram format (mobile-friendly) | ✅ | 2-line compact：天氣 + MTR ETA + 事故 |
| Cron 07:45 HKT weekday | ✅ | `gg-commute-morning` (ID: 5a87854cdc37) |
| 自訂目的地 (`--to 灣仔`) | ✅ | CLI param |
| 07:30 Morning Briefing 整合 | ✅ | 用 gg-commute 做 commute section |
| 08:00 DIGEST 整合 | ✅ | 用 gg-commute 代替舊 weather check |
| Future native MCP injection | 🔲 | 等 Hermes upstream support |

## MCP Servers (10 total, 62 tools)

| MCP | Tools | Source | 用途 |
|:----|:-----:|:------|:-----|
| **hkgov** 🏛️ | 6 | data.gov.hk | MTR ETA、KMB 268C、交通意外、公眾假期、通勤三合一 |
| **google-maps** 🗺️ | 15 | npm | 路線 planning、即時交通、place search |
| **notion** 📋 | 22 | npm | CRM、Task Center、Projects |
| **weather** 🌤️ | 3 | HKO | 即時天氣、7日預測 |
| **system** 📊 | 3 | local | VM metrics、cron status |
| **memory** 🧠 | 3 | local | hot.db FTS5 search |
| **calendar** 📅 | 3 | local | 今日/本週行程 |
| **sqlite** 💾 | 5 | npm | Upgrades registry、data queries |
| **github** 💻 | 5 | local | GGDev repo git ops |
| **apify** 🕸️ | 9 | npm | Web scraping |

## Key Files

- `~/.local/bin/gg-commute` — Unified wrapper script (Python, ~200 lines)
- `~/.local/bin/mcp-*-custom.py` — 6 custom MCP servers
- `~/.hermes/mcp_config.yaml` — MCP registration

## Architecture

```
User (Telegram)
    │
    ├─ cron 07:45 → gg-commute --format telegram → Telegram push
    ├─ cron 07:30 → Morning Briefing (includes gg-commute)
    └─ cron 08:00 → DIGEST (includes gg-commute)
    
gg-commute (Python wrapper)
    ├─ mcp-weather-custom.py   → HKO API
    ├─ mcp-hkgov-custom.py     → data.gov.hk (MTR + KMB + traffic)
    └─ (future) google-maps     → Maps API transit route
```

## Security

- ✅ All API keys in `~/.hermes/.env` (600 permissions)
- ✅ Zero hardcoded keys in scripts
- ⚠️ `~/.config/notion/api_key` — duplicate key, pending deletion
- ⚠️ Google Maps API key — add IP restriction

## Created

2026-05-30 | Status: active
