# SKILL: briefing-format

## Risk class
**Read** (format reference) — applied when GG prepares a daily briefing.

## Trigger
- Auto: when GG is running **morning briefing** (07:30 cron job)
- Auto: when GG is running **morning reminder** (08:00 cron job)
- Auto: when Terrence asks "brief me" or "今日有咩要知"
- Manual: Terrence says "俾briefing"

## Summary
Defines the format and content rules for GG's daily briefings. Ensures consistency across morning briefing (07:30) and morning reminder (08:00).

---

## 1. 07:30 Briefing — 天氣 + 日程 + 新聞

### Content (required)
1. **🌤 天氣** — HKO data（溫度、濕度、雨量、警告）
2. **📅 今日日程** — Reminders + Google Calendar + Notion tasks
3. **📰 今日重點** — 新聞摘要（只限相關話題）
4. **💡 提醒** — 如果今日有 overdue 或重要未完成事項

### Format (message 1 — weather + schedule)
```
🌅 **Good morning Terrence | {date} {weekday}**

**🌤 天氣**
• {temp}°C, {humidity}%, {condition}
• {warning if any}
• {rain chance if applicable}

**📅 今日行程**
• {time} {event} {location if any}
• {time} {event}
...
```

### Format (message 2 — news + reminders) — only if needed
```
**📰 今日重點**
• {item 1}
• {item 2}

**💡 提提你**
• {overdue/unfinished items}
```

### Buttons (mandatory)
- `✅ 收到` / `✏️ 改錯`

### Key rules
- Keep it concise — 2 messages max
- If nothing special, just message 1
- News only if relevant to Terrence (tech, HK, finance, church)
- Don't repeat what Terrence already knows (daily routine)

---

## 2. 08:00 Reminder — 屬靈 + 提醒 + 路面

### Content (required)
1. **🙏 屬靈提醒** — 今日有冇church activity / devotion reminder
2. **⏰ 重要提醒** — 今日關鍵事項（meetings, deadlines, appointments）
3. **🚗 路面狀況** — 如果今日要出街，check traffic

### Format (single message)
```
🌅 **早晨提醒 | {date} {weekday}**

**🙏 屬靈**
• {item}

**⏰ 今日提醒**
• {item}

**🚗 路面**
• {only if relevant}
```

### Buttons (mandatory)
- `✅ 收到` / `✏️ 改錯`

### Key rules
- 08:00 = actionable, not informational
- Focus on things Terrence needs to action TODAY
- Don't duplicate 07:30 briefing content — complement it

---

## 3. General rules (both briefings)

### Sources
- Weather: HKO skill (`hko-weather`)
- Schedule: Reminder state + Notion + Google Calendar
- Traffic: KMB/Citybus ETA skills + Google Maps API
- News: Tavily / Perplexity search (topic-relevant only)
- Church: Notion tasks / memory

### Order
- Always summary first (1-2 lines)
- Then detail
- End with action item / question if needed

### Tone
- Morning = calm, clear, not rushed
- Don't overwhelm — if nothing important, say "今日冇特別"
- Use bullets, not paragraphs

### Edge cases
- Holiday / weekend: Adjust to "今日休息日" tone
- Bad weather warning: Put it FIRST, before everything else
- No schedule: 一句「今日冇行程安排」就夠，唔好硬塞資訊
