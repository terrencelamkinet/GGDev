# SKILL: reminder-rules

## Risk class
**Read** (rules check) — no data modification; loaded on reminder delivery context.

## Trigger
- Auto: when processing a reminder delivery (daemon context)
- Auto: when user mentions "reminder", "button", "snooze", "推遲", "urgent"
- Manual: Terrence says "check reminder rules"

## Summary
Defines the complete behaviour for GG's reminder buttons, urgency tiers, and snooze durations. Everything Terrence has set about how reminders should work.

---

## 1. Button Layout (mandatory, all reminder types)

Every reminder message MUST have exactly these inline buttons:

```
✅ 做咗  ⏰ 推遲
❌ 取消
```

- **做咗 (confirm)** → state = dismissed, never remind again
- **推遲 (snooze)** → resend after snooze duration (see §2)
- **取消 (dismiss)** → state = dismissed, permanent stop

**Button rules** (from SOUL.md):
- Max 2 buttons per row
- Short label + clear meaning + icon last
- Use `exec gg_send.py` to send, never mix assistant reply with buttons
- Research backing: Fatigue Survey (ArXiv 2403) — user control reduces fatigue

---

## 2. Snooze Duration by Urgency

More urgent = shorter snooze (Terrence's rule, 2026-05-22).

| Tier | Snooze | When | Source |
|------|--------|------|--------|
| U1 ℹ️ FYI | 480min (next morning) | 48h+ before event | Terrence's rule 2026-05-22; Cortana logs (Horvitz 2016): distant events = reference only |
| U2 🟢 Normal | 720min (12h) | 2-47h before event | Terrence's rule 2026-05-22 |
| U3 🟡 Soon | 240min (4h) | <2h before event | Terrence's rule 2026-05-22; GG's internal operational definition for "approaching deadline" |
| U4 🔴 Now | 60min | Overdue / sent 2+h no response | Terrence's rule 2026-05-22 |
| U5 🔴🚨 Esc | 30min | 2nd+ resend attempt | Terrence's rule 2026-05-22; re-search via research-methodology.skill.md for latest evidence |

> **Note**: Tier thresholds (48h/2-47h/<2h) are GG system's operational definition for reminder classification, aligned with Cortana log analysis pattern (Horvitz 2016). The snooze durations (480/720/240/60/30 min) are Terrence's rules, determined 2026-05-22. See Case (2) in §Case studies.

**Override**: Quiet hours (22:00-07:59) → any snooze pushes to next morning (480min).

---

## 3. Urgency Tier Classification (Research-Backed)

| Tier | Name | Emoji | Research Basis |
|------|------|-------|----------------|
| 1 | FYI | ℹ️ | Cortana logs (Horvitz 2016): distant = reference only. JMIR Pirolli 2017: low freq = high freq for distant items. |
| 2 | Normal | ⏰ | JMIR 2017: reminders hours/days away don't need push. |
| 3 | Soon | ⌛️ | Gollwitzer Implementation Intentions: specific trigger+action effective. Cortana: same-day reminders most clicked. |
| 4 | Now | 🚨 | Springer "Now, Later, Never" 2022: time-sensitivity=primary urgency. PersoNo (IEEE ISMAR 2025): content+context=highest urgency. |
| 5 | Escalation | 🚨🚨 | Fatigue Survey (ArXiv 2403): >3 same topic = desensitisation. Cortana: 2nd reminder spaced >30min. |

**Computed by**: `gg_reminder_context.py` → `compute_urgency_tier()`

---

## 4. Quiet Hours Policy

- **22:00 - 07:59**: suppress non-urgent (U<4) deliveries
- **Research**: PersoNo (IEEE 2025) — activity context determines urgency. Fatigue Survey (ArXiv 2403) — night delivery suppresses next-day receptivity.
- **Implemented in**: `gg_reminder_daemon.py` quiet hours check

---

## 5. Resend (Overdue) Behaviour

- Grace period: 30min before sent→overdue
- Resend interval: 40min (research: >30min prevents desensitisation)
- Max 3 deliveries per topic per day (research: >3 = fatigue risk)
- Header changes per delivery: ⏰ → 🚨 → 🚨🚨 with "跟進第N次" suffix
- Delivery count tracked in `_last_resend_ts` and `delivery_count` fields

---

---

## 🎯 Case studies from Terrence's life

### (1) 2026-05-22: Inline buttons — second version
- Problem: First version had different buttons per source (calendar=3 buttons, notion=2, routine=3), causing confusion
- Terrence fix: All reminders = uniform 3-button layout: ✅ 做咗 / ⏰ 推遲 / ❌ 取消
- Result: Single layout, no context-switching, no confusion
- Lesson: User-facing UI must be consistent across all entry points. Source differences are backend concerns.

### (2) 2026-05-22: Snooze direction — research vs reality
- Problem: GG proposed inverted snooze (more urgent=longer space) citing Fatigue Survey (ArXiv 2403)
- Terrence: "錯曬" → more urgent MUST check back faster
- Final rule: U5=30min fastest, U2=720min slowest
- Lesson: Research informs; Terrence's actual usage and intuition overrides research.

### (3) 2026-05-22: Overdue resend frequency
- Problem: Multiple reminders stacking up on same day → noise
- Solution: Max 3 deliveries per topic/day, 40min interval between resends
- Research: Fatigue Survey (ArXiv 2403) — >3 same-topic = desensitisation

### (4) 2026-05-22: Quiet hours debate
- Problem: GG proposed suppressing ALL reminders 22:00-07:59
- Reality: Some reminders ARE urgent at night (e.g. church preparation the night before)
- Solution: Suppress U<4 only. U4+ still delivered.
- Lesson: Hard suppression rules need tier exception.

---

## ⚠️ Research note
The citations in the urgency tier table above were cited from memory. Before using these claims in decisions or documentation, re-search via `research-methodology.skill.md` to find current best sources.

## References
- Research methodology: `gg-skills/research-methodology.skill.md`
- Full research summary: `scripts/vm/gg_remitter_research.md`
- Source code: `gg_reminder_context.py` (compute_urgency_tier, build_reminder_header)
- Source code: `gg_reminder_daemon.py` (deliver_reminder, _build_inline_keyboard)
- State persistence: `~/.openclaw/logs/gg-reminder-state.json`
- Daemon: systemd `gg-reminder.service`, PID log at `~/.openclaw/logs/gg-reminder.pid`
