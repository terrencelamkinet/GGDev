***REMOVED*** Design Language: 3AI Intelligence Dashboard

> Extracted from `http://localhost:7870` on June 8, 2026
> 1325 elements analyzed

This document describes the complete design language of the website. It is structured for AI/LLM consumption — use it to faithfully recreate the visual design in any framework.

***REMOVED******REMOVED*** Color Palette

***REMOVED******REMOVED******REMOVED*** Primary Colors

| Role | Hex | RGB | HSL | Usage Count |
|------|-----|-----|-----|-------------|
| Primary | `***REMOVED***af52de` | rgb(175, 82, 222) | hsl(280, 68%, 60%) | 15 |
| Secondary | `***REMOVED***5856d6` | rgb(88, 86, 214) | hsl(241, 61%, 59%) | 35 |
| Accent | `***REMOVED***ff3b30` | rgb(255, 59, 48) | hsl(3, 100%, 59%) | 49 |

***REMOVED******REMOVED******REMOVED*** Neutral Colors

| Hex | HSL | Usage Count |
|-----|-----|-------------|
| `***REMOVED***3c3c43` | hsl(240, 6%, 25%) | 1148 |
| `***REMOVED***000000` | hsl(0, 0%, 0%) | 1119 |
| `***REMOVED***ffffff` | hsl(0, 0%, 100%) | 166 |
| `***REMOVED***787880` | hsl(240, 3%, 49%) | 107 |
| `***REMOVED***e5e5ea` | hsl(240, 11%, 91%) | 21 |
| `***REMOVED***f2f2f7` | hsl(240, 24%, 96%) | 1 |
| `***REMOVED***c6c6c8` | hsl(240, 2%, 78%) | 1 |

***REMOVED******REMOVED******REMOVED*** Background Colors

Used on large-area elements: `***REMOVED***f2f2f7`

***REMOVED******REMOVED******REMOVED*** Text Colors

Text color palette: `***REMOVED***000000`, `***REMOVED***ffffff`, `***REMOVED***3c3c43`, `***REMOVED***af52de`, `***REMOVED***34c759`, `***REMOVED***ff6b35`, `***REMOVED***5856d6`, `***REMOVED***ff2d55`, `***REMOVED***ff9500`, `***REMOVED***ff3b30`

***REMOVED******REMOVED******REMOVED*** Gradients

```css
background-image: linear-gradient(135deg, rgb(255, 107, 53), rgb(175, 82, 222));
```

***REMOVED******REMOVED******REMOVED*** Full Color Inventory

| Hex | Contexts | Count |
|-----|----------|-------|
| `***REMOVED***3c3c43` | text, border | 1148 |
| `***REMOVED***000000` | text, border | 1119 |
| `***REMOVED***ffffff` | text, border, background | 166 |
| `***REMOVED***34c759` | text, border, background | 143 |
| `***REMOVED***787880` | border | 107 |
| `***REMOVED***ff3b30` | text, border, background | 49 |
| `***REMOVED***5856d6` | background, border, text | 35 |
| `***REMOVED***e5e5ea` | background | 21 |
| `***REMOVED***ff6b35` | background, text, border | 20 |
| `***REMOVED***af52de` | background, text, border | 15 |
| `***REMOVED***ff9500` | background, border, text | 14 |
| `***REMOVED***ff2d55` | text, border | 12 |
| `***REMOVED***f2f2f7` | background | 1 |
| `***REMOVED***c6c6c8` | border | 1 |

***REMOVED******REMOVED*** Typography

***REMOVED******REMOVED******REMOVED*** Font Families

- **Arial** — used for body (30 elements)
- **SF Mono** — used for body (12 elements)
- **Times New Roman** — used for body (8 elements)

***REMOVED******REMOVED******REMOVED*** Type Scale

| Size (px) | Size (rem) | Weight | Line Height | Letter Spacing | Used On |
|-----------|------------|--------|-------------|----------------|---------|
| 28px | 1.75rem | 700 | 33.6px | normal | span |
| 24px | 1.5rem | 400 | normal | normal | div |
| 20px | 1.25rem | 700 | normal | normal | div, span |
| 18px | 1.125rem | 400 | normal | normal | button, svg, use, span |
| 17px | 1.0625rem | 700 | 22.1px | normal | h1, input |
| 16px | 1rem | 400 | normal | normal | html, head, meta, title |
| 15px | 0.9375rem | 700 | normal | normal | div, span |
| 13px | 0.8125rem | 400 | normal | normal | p, span, div, strong |
| 12px | 0.75rem | 400 | 16.2px | normal | div, span, template, strong |
| 11px | 0.6875rem | 400 | normal | 0.5px | div, span, td, button |
| 10px | 0.625rem | 600 | normal | 0.5px | span, div, th |
| 9px | 0.5625rem | 400 | normal | normal | span |

***REMOVED******REMOVED******REMOVED*** Heading Scale

```css
h1 { font-size: 17px; font-weight: 700; line-height: 22.1px; }
```

***REMOVED******REMOVED******REMOVED*** Body Text

```css
body { font-size: 12px; font-weight: 400; line-height: 16.2px; }
```

***REMOVED******REMOVED******REMOVED*** Font Weights in Use

`400` (1087x), `700` (94x), `500` (73x), `600` (71x)

***REMOVED******REMOVED*** Spacing

**Base unit:** 4px

| Token | Value | Rem |
|-------|-------|-----|
| spacing-1 | 1px | 0.0625rem |
| spacing-20 | 20px | 1.25rem |
| spacing-27 | 27px | 1.6875rem |
| spacing-32 | 32px | 2rem |
| spacing-48 | 48px | 3rem |
| spacing-444 | 444px | 27.75rem |

***REMOVED******REMOVED*** Border Radii

| Label | Value | Count |
|-------|-------|-------|
| md | 10px | 2 |
| lg | 13px | 105 |
| full | 50px | 91 |
| full | 999px | 22 |

***REMOVED******REMOVED*** Box Shadows

**sm** — blur: 8px
```css
box-shadow: rgb(175, 82, 222) 0px 0px 8px 0px;
```

***REMOVED******REMOVED*** CSS Custom Properties

***REMOVED******REMOVED******REMOVED*** Colors

```css
--secondarySystemBackground: ***REMOVED***2C2C2E;
--secondarySystemFill: rgba(120,120,128,0.32);
--secondaryLabel: rgba(235,235,245,0.6);
--radius-card: 13px;
```

***REMOVED******REMOVED******REMOVED*** Spacing

```css
--space-3xs: 2px;
--space-2xs: 4px;
--space-xs: 6px;
--space-sm: 8px;
--space-md: 12px;
--space-lg: 16px;
--space-xl: 20px;
--space-2xl: 20px;
--space-3xl: 32px;
--space-4xl: 40px;
--space-5xl: 48px;
```

***REMOVED******REMOVED******REMOVED*** Typography

```css
--font: -apple-system, 'SF Pro Text', 'SF Pro Display', 'Helvetica Neue', sans-serif;
--font-display: -apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif;
--font-mono: 'SF Mono', 'JetBrains Mono', 'Menlo', monospace;
```

***REMOVED******REMOVED******REMOVED*** Radii

```css
--radius-pill: 999px;
--radius-input: 10px;
--radius-tab: 7px;
```

***REMOVED******REMOVED******REMOVED*** Other

```css
--systemBackground: ***REMOVED***1C1C1E;
--tertiarySystemBackground: ***REMOVED***3A3A3C;
--groupedBackground: ***REMOVED***121214;
--systemFill: rgba(120,120,128,0.36);
--tertiarySystemFill: rgba(120,120,128,0.24);
--quaternarySystemFill: rgba(120,120,128,0.18);
--label: ***REMOVED***FFFFFF;
--tertiaryLabel: rgba(235,235,245,0.3);
--quaternaryLabel: rgba(235,235,245,0.18);
--regularMaterial: rgba(28,28,30,0.85);
--thinMaterial: rgba(28,28,30,0.7);
--ultraThinMaterial: rgba(28,28,30,0.5);
--systemBlue: ***REMOVED***0A84FF;
--systemGreen: ***REMOVED***30D158;
--systemRed: ***REMOVED***FF453A;
--systemOrange: ***REMOVED***FF9F0A;
--systemPurple: ***REMOVED***BF5AF2;
--systemPink: ***REMOVED***FF375F;
--systemGray: ***REMOVED***8E8E93;
--systemGray2: ***REMOVED***636366;
--systemGray3: ***REMOVED***48484A;
--systemGray4: ***REMOVED***3A3A3C;
--systemGray5: ***REMOVED***2C2C2E;
--systemGray6: ***REMOVED***1C1C1E;
--fighter: ***REMOVED***FF6B35;
--work: ***REMOVED***5E5CE6;
--person: ***REMOVED***FF375F;
--pplx: ***REMOVED***BF5AF2;
--separator: rgba(84,84,86,0.6);
--opaqueSeparator: ***REMOVED***38383A;
--safe-top: env(safe-area-inset-top, 20px);
--safe-bottom: env(safe-area-inset-bottom, 0px);
--tab-height: 50px;
--largeTitle: 34px;
--title1: 28px;
--title2: 22px;
--title3: 20px;
--headline: 17px;
--body: 17px;
--callout: 16px;
--subheadline: 15px;
--footnote: 13px;
--caption: 12px;
--caption2: 11px;
```

***REMOVED******REMOVED******REMOVED*** Semantic

```css
success: [object Object];
warning: [object Object];
error: [object Object];
info: [object Object];
```

***REMOVED******REMOVED*** Transitions & Animations

**Durations:** `0.2s`, `0.15s`

***REMOVED******REMOVED******REMOVED*** Common Transitions

```css
transition: all;
transition: -webkit-line-clamp 0.2s, max-height 0.2s;
transition: border-color 0.2s;
transition: opacity 0.15s;
transition: 0.2s;
transition: color 0.2s;
```

***REMOVED******REMOVED******REMOVED*** Keyframe Animations

**breathe**
```css
@keyframes breathe {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}
```

**shimmer**
```css
@keyframes shimmer {
  0% { background-position: 200% 0px; }
  100% { background-position: -200% 0px; }
}
```

**fadeIn**
```css
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0px); }
}
```

**spin**
```css
@keyframes spin {
  100% { transform: rotate(360deg); }
}
```

***REMOVED******REMOVED*** Component Patterns

Detected UI component patterns and their most common styles:

***REMOVED******REMOVED******REMOVED*** Buttons (9 instances)

```css
.button {
  background-color: rgb(175, 82, 222);
  color: rgba(60, 60, 67, 0.3);
  font-size: 11px;
  font-weight: 400;
  padding-top: 0px;
  padding-right: 0px;
  border-radius: 0px;
}
```

***REMOVED******REMOVED******REMOVED*** Cards (70 instances)

```css
.card {
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 0px;
  box-shadow: rgb(175, 82, 222) 0px 0px 8px 0px;
  padding-top: 0px;
  padding-right: 0px;
}
```

***REMOVED******REMOVED******REMOVED*** Inputs (1 instances)

```css
.input {
  background-color: rgb(255, 255, 255);
  color: rgb(0, 0, 0);
  border-color: rgba(60, 60, 67, 0.29);
  border-radius: 10px;
  font-size: 17px;
  padding-top: 10px;
  padding-right: 14px;
}
```

***REMOVED******REMOVED******REMOVED*** Navigation (3 instances)

```css
.navigatio {
  color: rgb(0, 0, 0);
  padding-top: 0px;
  padding-bottom: 0px;
  padding-left: 0px;
  padding-right: 0px;
  position: static;
}
```

***REMOVED******REMOVED******REMOVED*** Tables (1 instances)

```css
.table {
  border-color: rgb(128, 128, 128);
  cell-style: [object Object];
}
```

***REMOVED******REMOVED******REMOVED*** Badges (17 instances)

```css
.badge {
  color: rgba(60, 60, 67, 0.3);
  font-size: 11px;
  font-weight: 400;
  padding-top: 0px;
  padding-right: 0px;
  border-radius: 0px;
}
```

***REMOVED******REMOVED******REMOVED*** Avatars (1 instances)

```css
.avatar {
  border-radius: 50%;
}
```

***REMOVED******REMOVED******REMOVED*** Tabs (22 instances)

```css
.tab {
  background-color: rgba(255, 255, 255, 0.85);
  color: rgba(60, 60, 67, 0.3);
  font-size: 11px;
  font-weight: 400;
  padding-top: 0px;
  padding-right: 0px;
  border-color: rgba(60, 60, 67, 0.3);
  border-radius: 0px;
}
```

***REMOVED******REMOVED*** Component Clusters

Reusable component instances grouped by DOM structure and style similarity:

***REMOVED******REMOVED******REMOVED*** Card — 6 instances, 2 variants

**Variant 1** (3 instances)

```css
  background: rgba(255, 255, 255, 0.7);
  color: rgb(0, 0, 0);
  padding: 12px 12px 12px 12px;
  border-radius: 13px;
  border: 1px solid rgba(120, 120, 128, 0.18);
  font-size: 16px;
  font-weight: 400;
```

**Variant 2** (3 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(0, 0, 0);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(0, 0, 0);
  font-size: 16px;
  font-weight: 400;
```

***REMOVED******REMOVED******REMOVED*** Card — 3 instances, 1 variant

**Variant 1** (3 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(0, 0, 0);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(0, 0, 0);
  font-size: 16px;
  font-weight: 400;
```

***REMOVED******REMOVED******REMOVED*** Card — 3 instances, 1 variant

**Variant 1** (3 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(0, 0, 0);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(0, 0, 0);
  font-size: 13px;
  font-weight: 600;
```

***REMOVED******REMOVED******REMOVED*** Card — 3 instances, 1 variant

**Variant 1** (3 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgba(60, 60, 67, 0.6);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgba(60, 60, 67, 0.6);
  font-size: 12px;
  font-weight: 400;
```

***REMOVED******REMOVED******REMOVED*** Button — 5 instances, 2 variants

**Variant 1** (1 instance)

```css
  background: rgba(0, 0, 0, 0);
  color: rgb(0, 0, 0);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgb(0, 0, 0);
  font-size: 11px;
  font-weight: 400;
```

**Variant 2** (4 instances)

```css
  background: rgba(0, 0, 0, 0);
  color: rgba(60, 60, 67, 0.3);
  padding: 0px 0px 0px 0px;
  border-radius: 0px;
  border: 0px none rgba(60, 60, 67, 0.3);
  font-size: 11px;
  font-weight: 400;
```

***REMOVED******REMOVED*** Layout System

**2 grid containers** and **114 flex containers** detected.

***REMOVED******REMOVED******REMOVED*** Container Widths

| Max Width | Padding |
|-----------|---------|
| 393px | 0px |

***REMOVED******REMOVED******REMOVED*** Grid Column Patterns

| Columns | Usage Count |
|---------|-------------|
| 3-column | 2x |

***REMOVED******REMOVED******REMOVED*** Grid Templates

```css
grid-template-columns: 112.328px 112.328px 112.344px;
gap: 8px;
grid-template-columns: 112.328px 112.328px 112.344px;
gap: 8px;
```

***REMOVED******REMOVED******REMOVED*** Flex Patterns

| Direction/Wrap | Count |
|----------------|-------|
| column/nowrap | 28x |
| row/nowrap | 85x |
| row/wrap | 1x |

**Gap values:** `16px`, `20px`, `2px`, `4px`, `8px`

***REMOVED******REMOVED*** Accessibility (WCAG 2.1)

**Overall Score: 100%** — 1 passing, 0 failing color pairs

***REMOVED******REMOVED******REMOVED*** Passing Color Pairs

| Foreground | Background | Ratio | Level |
|------------|------------|-------|-------|
| `***REMOVED***ffffff` | `***REMOVED***5856d6` | 5.65:1 | AA |

***REMOVED******REMOVED*** Design System Score

**Overall: 89/100 (Grade: B)**

| Category | Score |
|----------|-------|
| Color Discipline | 92/100 |
| Typography Consistency | 80/100 |
| Spacing System | 85/100 |
| Shadow Consistency | 100/100 |
| Border Radius Consistency | 100/100 |
| Accessibility | 100/100 |
| CSS Tokenization | 100/100 |

**Strengths:** Tight, disciplined color palette, Well-defined spacing scale, Clean elevation system, Consistent border radii, Strong accessibility compliance, Good CSS variable tokenization

**Issues:**
- 9 !important rules — prefer specificity over overrides
- 50% of CSS is unused — consider purging
- 273 duplicate CSS declarations

***REMOVED******REMOVED*** Gradients

**1 unique gradients** detected.

| Type | Direction | Stops | Classification |
|------|-----------|-------|----------------|
| linear | 135deg | 2 | brand |

```css
background: linear-gradient(135deg, rgb(255, 107, 53), rgb(175, 82, 222));
```

***REMOVED******REMOVED*** SVG Icons

**7 unique SVG icons** detected. Dominant style: **filled**.

| Size Class | Count |
|------------|-------|
| sm | 3 |
| md | 4 |

**Icon colors:** `rgb(0, 0, 0)`

***REMOVED******REMOVED*** Motion Language

**Feel:** mixed · **Scroll-linked:** yes

***REMOVED******REMOVED******REMOVED*** Duration Tokens

| name | value | ms |
|---|---|---|
| `xs` | `150ms` | 150 |
| `sm` | `200ms` | 200 |

***REMOVED******REMOVED******REMOVED*** Keyframes In Use

| name | kind | properties | uses |
|---|---|---|---|
| `breathe` | reveal | opacity, transform | 4 |
| `fadeIn` | slide-y | opacity, transform | 46 |
| `spin` | rotate | transform | 1 |

***REMOVED******REMOVED*** Component Anatomy

***REMOVED******REMOVED******REMOVED*** card — 15 instances


***REMOVED******REMOVED******REMOVED*** button — 5 instances

**Slots:** label, icon

***REMOVED******REMOVED*** Brand Voice

**Tone:** neutral · **Pronoun:** third-person · **Headings:** unknown (tight)

***REMOVED******REMOVED******REMOVED*** Top CTA Verbs

- **home** (1)
- **intelligence** (1)
- **tasks** (1)
- **connection** (1)
- **settings** (1)

***REMOVED******REMOVED******REMOVED*** Button Copy Patterns

- "home" (1×)
- "intelligence" (1×)
- "tasks" (1×)
- "connection" (1×)
- "settings" (1×)

***REMOVED******REMOVED*** Page Intent

**Type:** `landing` (confidence 0.45)

***REMOVED******REMOVED*** Material Language

**Label:** `material-you` (confidence 0.45)

| Metric | Value |
|--------|-------|
| Avg saturation | 0.401 |
| Shadow profile | soft |
| Avg shadow blur | 0px |
| Max radius | 999px |
| backdrop-filter in use | no |
| Gradients | 1 |

***REMOVED******REMOVED*** Quick Start

To recreate this design in a new project:

1. **Install fonts:** Add `Arial` from Google Fonts or your font provider
2. **Import CSS variables:** Copy `variables.css` into your project
3. **Tailwind users:** Use the generated `tailwind.config.js` to extend your theme
4. **Design tokens:** Import `design-tokens.json` for tooling integration
