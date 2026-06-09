# GG Dashboard v2.0

**Release:** 2026-06-09
**Previous:** v1.2 (Apple HIG + iPhone 14 Pro guideline compliance)
**Purpose:** Complete iOS-native rewrite — Apple HIG 100% compliance

## v2.0 — Full iOS-Native Rewrite

### Design System (Complete CSS Rewrite)
- **Apple iOS System Colors**: Replaced all custom colors with Apple's `--system-background: #1C1C1E`, `--secondary-background: #2C2C2E`, `--tertiary-background: #3A3A3C`, `--separator: rgba(84,84,88,0.36)`, `--label: #FFFFFF`, `--secondary-label`, `--tertiary-label`, `--quaternary-label`, `--fill`, `--secondary-fill`, `--tertiary-fill` — fully dark/light compatible
- **iOS Typography Scale**: Added `.ios-large-title` (34pt), `.ios-title-1` (28pt), `.ios-title-2` (22pt), `.ios-title-3` (20pt), `.ios-headline` (17pt), `.ios-body` (17pt), `.ios-callout` (16pt), `.ios-subhead` (15pt), `.ios-footnote` (13pt), `.ios-caption-1` (12pt), `.ios-caption-2` (11pt) — matching Apple HIG font sizes, weights, and letter-spacing
- **SF Pro Font Stack**: `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text'` as primary typeface

### App Shell — iPhone 14 Pro (393px)
- `.app-shell` max-width 393px matching iPhone 14 Pro viewport
- All body text at 17px (iOS default reading size)
- Background uses `--system-background` / `--secondary-background` (iOS grouped list style)

### iOS Navigation Bar (Large Title Style)
- `.nav-bar` with sticky positioning, `calc(12px + var(--safe-top))` padding
- `backdrop-filter: saturate(180%) blur(20px)` for native frosted glass
- `.page-title` at 34px Large Title weight, `.page-subtitle` at 15px
- Light mode: `rgba(249,249,249,0.92)` background

### iOS Inset Grouped List Sections
- `.ios-section` + `.ios-header` (13px uppercase, letter-spacing 0.7px) + `.ios-group` (10px border-radius)
- `.ios-row` with 44px min-height, 0.5px hairline separators, flex layout
- `.ios-row-content` with `.ios-row-label` (17px body) + `.ios-row-meta` (13px footnote)
- `.ios-row-trailing` for right-aligned content

### iOS Tab Bar (Exactly 49pt)
- `.ios-tab-bar` fixed at bottom, `calc(49px + var(--safe-bottom))` height
- 25px tab icons, 10px tab labels, `rgba(28,28,30,0.92)` frosted glass
- Active state: accent color for both icon and label

### iOS Stat Cards
- `.ios-stats` 4-column grid with 0.5px separator gaps
- `.ios-stat-value` at 22px Title 2 weight, `.ios-stat-label` at 11px Caption 2

### iOS Filter Chips (Segmented Control Style)
- `.ios-filter-row` with `.ios-chip` (15px, 8px radius, 44px touch targets)
- Active state: accent fill with white text

### Template Rewrites (All 5 Pages)

**home.html**: iOS nav bar with Good Morning/Afternoon/Evening, 4-stat iOS grid, "AI Intelligence" section with inset group, "Servants" section as 3 iOS rows with colored dots, chevron indicators

**tasks.html**: iOS filter chips (All/Work/Personal/Learning), task list as iOS rows with check circles, detail overlay with iOS sheet styling, edit panel as bottom sheet with handle

**intel.html**: iOS search bar (rounded, transparent bg), "GG Voices" as iOS rows with colored dots, "Discoveries" as iOS rows, "Activity Stream" as iOS rows

**agents.html**: 3 agent rows in iOS group with colored dots + status badges, "Right Now" thoughts section, "Tracked Needs" resource section

**profile.html**: Identity card as iOS row with avatar, "Personal" section with 4 info rows, "System" section with 5 data rows

### Other iOS Features
- **Hairline Separators**: All borders use 0.5px (standard iOS hairline)
- **Touch Targets**: All interactive elements maintain 44px min-height
- **Safe Areas**: `env(safe-area-inset-top/bottom)` on nav bar, tab bar, overlays
- **Pull-to-Refresh**: Touch scrolling with `-webkit-overflow-scrolling: touch`
- **iOS Focus States**: `input:focus { outline: none; border-color: var(--accent); }`
- **Toast**: iOS-style bottom banner with blur backdrop
- **Chat Bubble**: iOS-style FAB with accent gradient

### Removed Legacy Classes
- All `.card`, `.card-header`, `.card-bg`, `.stat-card`, `.stat-grid-4`, `.top-bar`, `.header`, `.header-right`
- `.badge`, `.time-label`, `.metric-card`, `.metric-summary`, `.greeting`, `.nav-item`, `.nav-tab`
- `.col2`, `.col3`, `.section-title`, `.filter-row` (replaced with `.ios-filter-row`)
- Empty CSS classes eliminated; total CSS size reduced from ~13KB to ~18KB (more comprehensive)

### API Unchanged
- `app.py` — untouched, all endpoints preserved
- All existing JavaScript logic preserved, only HTML/CSS restructured

---

# GG Dashboard v1.2

**Release:** 2026-06-09
**Previous:** v1.1 (CSS refactor + WCAG AA fix)
**Purpose:** Apple HIG + iPhone 14 Pro guideline compliance (14 fixes)

## v1.2 Changes
- **CRITICAL — Input font-size 17px**: All input/textarea/select set to 17px (iOS zoom prevention). Global `body { font-size: 17px }` added. `-webkit-appearance: none; appearance: none;` applied to all form elements.
- **CRITICAL — Touch targets 44px**: `.filter-chip`, `.btn` given `min-height: 44px`. Detail close button → 44×44px. Intel search/deep buttons → `min-height: 44px`. Checkbox wrapped in `.chk-wrap` (44×44px hit area).
- **CRITICAL — Top-bar sticky + safe-area**: `.top-bar` now `position: sticky; top: 0; z-index: 10` with `calc(16px + var(--safe-top))` padding.
- **CRITICAL — Responsive grid**: `.col3` now switches to 1-column on ≤420px viewports. Agents cards + GG Voices stack vertically on mobile.
- **CRITICAL — Checkbox hit-area**: `.chk-wrap` (44×44px flex-centered wrapper) encloses `.chk-circle` with `pointer-events: none` for visual.
- **CRITICAL — Light mode bottom nav contrast**: Background changed from `rgba(255,255,255,0.85)` to `rgba(248,249,252,0.92)`.
- **HIGH — Edit panel safe area**: `padding-bottom: calc(20px + var(--sab))`.
- **HIGH — Detail overlay safe area**: `padding: max(60px, var(--sat)) 20px max(100px, var(--sab))`.
- **HIGH — Tap highlight disabled**: `-webkit-tap-highlight-color: transparent` on universal selector.
- **HIGH — Reduced motion**: WAAPI card animation checks `prefers-reduced-motion: reduce` and skips if active. CSS `@media (prefers-reduced-motion: reduce)` zeroes all animation/transition durations.
- **MEDIUM — WebApp meta tags**: `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `apple-mobile-web-app-title` added to all 5 page templates.
- **MEDIUM — SVG aria-labels**: All 25 bottom-nav `<svg class="icon-nav">` elements given `role="img"` and `aria-label="Home|Tasks|Intel|Agents|Profile"`.

---

# GG Dashboard v1.1

**Release:** 2026-06-08
**Previous:** v1.0 (designlang extraction baseline + initial CSS cleanup)
**CSS refactor:** -4,090 bytes, from 5,718 → 1,628 (71% reduction), duplicate declarations eliminated
**a11y fix:** time-label contrast 1.67:1 → 5.9:1 (AA pass)

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

## Infra
- Flask on :7870
- Cloudflare tunnel: intel.kinet-poc.com
- designlang MCP available for future cleanup
