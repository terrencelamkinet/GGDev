# Design Language Extraction — V1.0

**Date:** 2026-06-08
**Source:** `designlang --full http://localhost:7870 --out design-extract-output/`
**Generator:** designlang v7.0.0
**Dashboard:** GG Dashboard (Flask + Dribbble design)

## Files (24 total)

| File | Description | Lines |
|------|-------------|-------|
| `gg-dashboard-design-language.md` | Natural language design system spec | 643 |
| `gg-dashboard-design-tokens.json` | DTCG token spec (color, spacing, typography, radius) | 213 |
| `gg-dashboard-variables.css` | CSS custom properties | 138 |
| `gg-dashboard-mcp.json` | MCP server registration bindings | 461 |
| `gg-dashboard-figma-variables.json` | Figma variable bindings | — |
| `gg-dashboard-brand.html` | Brand extraction HTML | — |
| `gg-dashboard-theme.js` | Theme JavaScript | — |
| `gg-dashboard-tailwind-config.js` | Tailwind config | — |
| `gg-dashboard-tailwind-v4.css` | Tailwind v4 output | — |
| `gg-dashboard-reset.css` | CSS reset | — |
| `gg-dashboard-shadcn-theme.css` | shadcn/ui theme | — |
| `gg-dashboard-motion.framer.js` | Framer motion tokens | — |
| `gg-dashboard-motion.html` | Motion HTML | — |
| `gg-dashboard-motion-tokens.json` | Motion token spec | — |
| `gg-dashboard-gradients.css` | Gradient CSS | — |
| `gg-dashboard-gradients.json` | Gradient tokens | — |
| `gg-dashboard-icon-system.json` | Icon system (17 Lucide icons) | — |
| `gg-dashboard-form-states.json` | Form interaction states | — |
| `gg-dashboard-stack-intel.json` | Tech stack intelligence | — |
| `gg-dashboard-design-system.md` | Design system reference | — |
| `gg-dashboard-visual-dna.json` | Visual identity DNA | — |
| `gg-dashboard-voice.json` | Brand voice | — |
| `gg-dashboard-seo.json` | SEO metadata | — |
| `gg-dashboard-wordpress-theme.json` | WordPress theme export | — |
| `screenshots/` | Page screenshots (light mode only) | — |

## Key Findings (V1.0 → V1.1)

- **50% unused CSS rules** in styles.css
- **273 duplicate CSS declarations**
- **Container width inconsistency** — mixed `393px` vs `480px` max-width
- **Dark mode tokens not captured** — extraction only indexed light mode
- **0 failing contrast pairs** per WCAG analysis

## Querying

Use `designlang` MCP tools to query:
- `search_tokens("color")` — find all color tokens
- `find_nearest_color("#af52de", "AA-normal")` — find accessible palette color
- `list_failing_contrast_pairs()` — accessibility issues
- `get_component("card")` — component spec with variants

## Next

**V1.1** — CSS cleanup using extraction data:
- Delete unused CSS rules (~50% of current file)
- Merge duplicate declarations (~273 instances)
- Standardize container width to 393px
- Re-extract with `--dark` flag for dark mode tokens
