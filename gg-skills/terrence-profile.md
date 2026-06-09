# Terrence Pattern Profile

## Purpose
Build a detailed profile of Terrence's behaviour, communication style, busy times, and preferences — so GG can adapt proactively instead of reactively.

> **Note**: This is a non-invasive profile built only from interaction data that Terrence has consented to. No hidden tracking.

---

## 0. Personality Framework: Enneagram 7w6

### Core Traits (7 = Enthusiast, w6 = Loyalist wing)
| Trait | How it shows | GG adaptation |
|-------|-------------|---------------|
| **Novelty-seeking** | Enjoys new ideas, frameworks, systems thinking | Present changes as improvements, not corrections. Frame "fixes" as "upgrades". |
| **Strategic thinking** | Sees big picture, connects dots | Don't just give facts — explain how they connect to the larger system. |
| **Fear of missing out** | Wants to make sure no angle is missed | When proposing changes, cover edge cases proactively. |
| **Loyalty (w6)** | Once committed, sticks with what works | Don't suggest changes to stable systems without strong rationale. |
| **Anxiety (w6)** | Over-thinks decisions, wants validation | After proposing a plan, invite scrutiny — "think about any risk I missed." |
| **Skeptical (w6)** | Tests proposals before accepting | Expect to be questioned. Prepare thorough reasoning. |
| **Need for variety** | Multiple projects, interests, ideas | When organising tasks, offer options and prioritisation, not just a fixed list. |
| **Present-focused** | Responds to immediate, tangible needs | Avoid abstract theorising; anchor recommendations in "today's context." |

### Communication style implications
- **Wants depth, not fluff** — goes with "實用直接，唔繞圈" rule
- **Likes frameworks** — explains things in structured systems (九型、urgency tiers、decision framework)
- **Responds to evidence** — 7w6 appreciates both big-picture logic (7) AND detailed verification (w6)
- **Correction style**: Direct ("錯曬"), but expects you to learn from it (loyalty = invests in your growth)
- **Time awareness**: Knows when to push (深夜仲可以傾) and when to stop (quiet hours)

---

## 1. Communication Patterns

### Preferred Time
| Period | Activity | Notes |
|--------|----------|-------|
| Morning (07:00-09:00) | Daily briefing + planning | Brief, actionable preferred |
| Work hours (09:00-13:00) | Meetings, deep work | Minimal interruption preferred |
| Lunch (13:00-14:00) | Break | Light reminders OK |
| Afternoon (14:00-18:00) | Meetings, project work | Keep essential comms only |
| Evening (18:00-22:00) | Family / personal / church | Fewer work topics |
| Night (22:00-07:00) | Rest / can also be thinking time | Quiet hours for reminders OK, but conversational replies still welcome |

### Response Style
- **Tone**: Direct, practical, no small talk
- **Language**: Written Cantonese with HK flavour
- **7w6 pattern**: Detailed corrections (w6 precision) + big-picture thinking (7 vision)

---

## 2. Busy / Focus Indicators

### Location-aware logic
If context includes location info (via Google Calendar or explicit mention), adjust GG behaviour:

| Location | Likely Mode | GG Adaptation |
|----------|------------|---------------|
| 辦公室 / 觀塘 / AIA | Work mode | Keep comms brief, work-related only |
| 錦田 / 屋企 / 水尾村 | Home mode | Can be more casual, family topics OK |
| 教會 / Church | Church mode | Church-related only, respect activity |
| 街上 / driving / 揸車中 | Distracted | Keep ultra-brief, no decisions needed |
| 餐廳 / Cafe | Social / break | Light topics, no urgency |
| Unknown (only time given) | Default | Use time-of-day + reply pattern to infer |

### Signals GG is learning to detect
| Signal | Likely State | GG Action |
|--------|-------------|-----------|
| One-word replies (✅, ok, done, no) | Busy / doesn't want to engage | Keep reply minimal, no follow-ups |
| No reply within 2h of GG message | Deep focus / meeting | Don't resend; wait for natural reply |
| Short interval messages (multiple in <1min) | Rushing / urgent | Prioritise, keep brief |
| Late night messages (23:00+) | Thinking time (7w6: processing ideas) | GO AHEAD — 7w6 is often most creative/social at night. Don't assume "rest." |
| Weekend messages | Usually free | More conversational OK |
| Sunday | Church day | Church-related topics recommended |
| Location = 教會 during service time | Do not disturb | Defer all notifications |

### To track over time
- [ ] Average reply latency per time of day
- [ ] Message length patterns (short→busy, long→free)
- [ ] Topics that get quick replies vs delayed replies
- [ ] Time of day for different topics (work vs personal vs family)
- [ ] Weekend vs weekday pattern
- [ ] Location influence on reply speed and content

---

## 3. Interests & Knowledge Areas

### Work
- **Industry**: IT / Cybersecurity / Government projects
- **Tools**: Google Calendar, Notion, Kinetix, MTR, tunnel boring
- **Languages**: English (technical), Cantonese (daily)

### Personal
- **Activities**: Church (Sunday school, worship, teaching), family, car maintenance, 港車北上
- **Family**: Aggie (wife), mother
- **Transport**: Drives (own car), HK public transport
- **Current projects**: CCTV installation, SOW writing, HA meetings
- **7w6 interest pattern**: Multiple concurrent projects (7) but sees each through with attention to detail (w6)

---

## 4. Preferred Notification Style

From reminder-state.json analysis (2026-05-22):
- **Frequency**: Max 3 deliveries per topic/day, 40min min between resends
- **Tone**: Graduated (ℹ️ → ⏰ → ⌛️ → 🚨 → 🚨🚨)
- **Buttons**: Uniform 3-button: ✅ 做咗 / ⏰ 推遲 / ❌ 取消
- **Quiet hours**: 22:00-07:59 for reminders (but conversational replies still welcome)
- **Snooze**: Urgent = shorter delay (U5=30min fastest)
- **7w6 impact**: Wants control over timing (7 hates feeling constrained) + clear verification path (w6 needs to confirm)

### To track
- [ ] Which types of reminders get ✅ confirm first tap
- [ ] Which get ⏰ snoozed repeatedly
- [ ] Which get ❌ cancelled
- [ ] Time of day most receptive to notifications
- [ ] Location influence on reminder response

---

## 5. Learning Method

The profile is **never static** — GG updates it when:
1. Terrence corrects something → document the correction + update pattern
2. Terrence asks "點先做得更好" → add a new tracking dimension
3. A pattern appears 3+ times → record as likely trait
4. A correction appears 2+ times → flag as skill gap, ask Terrence to confirm
5. Terrence shares new self-info (e.g. Enneagram type) → integrate into profile framework

**Respect privacy**:
- Profile is stored in GG-Person memory (not GG-Work)
- Never shared with third parties
- Terrence can ask to see/delete/edit the profile anytime

---

## 6. Tracked Data Reference

Tracked via: `scripts/vm/track_patterns.py`
Patterns file: `gg-skills/terrence-patterns.json`
Format: timestamp, hour, day, text length, topic, latency

> ⚠️ This file tracks interaction metadata only (timing, length, topic). Never message content.
