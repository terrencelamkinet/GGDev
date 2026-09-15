# G03 — AI Dashboard File Inventory

## Source: `projects/ggdev-repo/gg-dashboard/`

## Backend

| File | Size | Purpose |
|------|------|---------|
| `code/app.py` | 941 lines | Flask backend (routes, API, data) |
| `code/hermes-config.yaml` | — | Hermes agent config |
| `code/hermes_update_data.py` | — | Data update script via Hermes |
| `code/gg_insights_collector.py` | — | AI insights collector |
| `code/gg_insights_pusher.py` | — | Insights push script |
| `code/patch_updater.py` | — | Patch updater utility |
| `code/update-memory-stats.py` | — | Memory stats updater |
| `code/update-maintenance.py` | — | Maintenance data updater |
| `code/update-data.sh` | — | Data update shell script |

## Data Files

| File | Purpose |
|------|---------|
| `code/gg-data.json` | Main dashboard data (refreshed every 15min) |
| `code/gg-insights.json` | AI intelligence insights data |
| `code/gg-memory-stats.json` | Memory statistics |
| `code/gg-maintenance.json` | Maintenance records |
| `code/gg_data.json` | Additional data (legacy) |

## Templates (8 HTML files)

| File | Purpose |
|------|---------|
| `code/templates/base.html` | Base template with iOS shell |
| `code/templates/home.html` | Dashboard home page |
| `code/templates/tasks.html` | Task management page |
| `code/templates/intel.html` | Intelligence feed page |
| `code/templates/agents.html` | AI agents/roles page |
| `code/templates/agent_detail.html` | Agent detail view |
| `code/templates/profile.html` | System profile page |
| `code/templates/aria.html` | (test/app page) |

## Static Files

| File | Purpose |
|------|---------|
| `code/static/styles.css` | Main stylesheet (iOS HIG design) |
| `code/static/notice-icons.svg` | SVG notice/notification icons |
| `code/static/icons.svg` | SVG icon sprite |
| `code/static/icons/` | 25 individual SVG icons |

## Design System & Extracts

| File | Purpose |
|------|---------|
| `code/design-extract/gg-dashboard-DESIGN.md` | Design system overview |
| `code/design-extract/gg-dashboard-design-language.md` | Design language documentation |
| `code/design-extract/gg-dashboard-visual-dna.json` | Visual DNA tokens |
| `code/design-extract/gg-dashboard-design-tokens.json` | Complete design tokens |
| `code/design-extract/gg-dashboard-tokens.d.ts` | Design tokens TypeScript types |
| `code/design-extract/gg-dashboard-variables.css` | CSS custom properties |
| `code/design-extract/gg-dashboard-tailwind-v4.css` | Tailwind v4 config |
| `code/design-extract/gg-dashboard-tailwind.config.js` | Tailwind config |
| `code/design-extract/gg-dashboard-shadcn-theme.css` | shadcn/ui theme |
| `code/design-extract/gg-dashboard-reset.css` | CSS reset |
| `code/design-extract/gg-dashboard-motion-tokens.json` | Motion/animation tokens |
| `code/design-extract/gg-dashboard-motion.html` | Motion examples |
| `code/design-extract/gg-dashboard-motion.framer.js` | Framer motion config |
| `code/design-extract/gg-dashboard-gradients.json` | Gradient definitions |
| `code/design-extract/gg-dashboard-gradients.css` | Gradient CSS |
| `code/design-extract/gg-dashboard-figma-variables.json` | Figma variables export |
| `code/design-extract/gg-dashboard-stack-intel.json` | Stack intelligence data |
| `code/design-extract/gg-dashboard-seo.json` | SEO metadata |
| `code/design-extract/gg-dashboard-icon-system.json` | Icon system spec |
| `code/design-extract/gg-dashboard-form-states.json` | Form state definitions |
| `code/design-extract/gg-dashboard-intent.json` | User intent mapping |
| `code/design-extract/gg-dashboard-library.json` | Design library manifest |
| `code/design-extract/gg-dashboard-voice.json` | Voice & tone guide |
| `code/design-extract/gg-dashboard-AGENT.md` | Agent instructions for design |
| `code/design-extract/gg-dashboard-brand.html` | Brand guidelines |
| `code/design-extract/gg-dashboard-preview.html` | Design preview page |
| `code/design-extract/gg-dashboard-theme.js` | Theme JS config |
| `code/design-extract/gg-dashboard-anatomy.tsx` | Component anatomy (TSX) |
| `code/design-extract/gg-dashboard-wordpress-theme.json` | WordPress theme config |
| `code/design-extract/gg-dashboard-mcp.json` | MCP server config |
| `code/design-extract/screenshots/` | Screenshots (full-page.png, card.png) |
| `code/design-extract/VERSION.md` | Design extract version history |
| `code/design-extract/gg-dashboard-prompts/` | AI prompts (cursor.md, v0.txt, lovable.txt, claude-artifacts.md, recipe-card.md, recipe-button.md) |

## Scripts

| File | Purpose |
|------|---------|
| `code/scripts/css_class_audit.py` | CSS class audit utility |

## Docs

| File | Size | Purpose |
|------|------|---------|
| `VERSION.md` | 7.4KB | Full version history (v1.1 → v1.2 → v2.0) |
| `CONTEXT.md` | — | Project context (preserved) |
| `KINETIX-RESPONSIBILITY.md` | — | Kinetix responsibilities doc |

## Fubon-Kong Related

| File | Purpose |
|------|---------|
| `code/fubon-kong-test-cases.csv` | Test cases CSV |
| `code/fubon-kong-test-cases.md` | Test cases markdown |
| `code/fubon-kong-test-flows.csv` | Test flows CSV |
| `code/fubon-kong-checklist-status.csv` | Checklist status CSV |
| `code/fubon-kong-checklist-mapping.md` | Checklist mapping |
| `code/fubon-kong-outstanding-features.md` | Outstanding features list |

## Other

| File | Purpose |
|------|---------|
| `code/test.html` | Test page |
| `code/launch.html` | Launch page |
| `code/bookmarklet.html` | Bookmarklet |
| `code/revert_test.md` | Revert test note |
