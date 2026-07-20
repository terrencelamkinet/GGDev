# KONGGER Web

**Social Platform Frontend** — a sellable, white-label HTML/JS frontend template.

Connects to any [kongger-api](https://github.com/terrencelamkinet/kongger-api) instance via configurable API base URL. Ready for instant rebranding and custom theming.

## Quick Start

1. Open `index.html` in a browser, OR
2. Serve with any static server:
   ```bash
   python3 -m http.server 8080
   # or
   npx serve .
   ```

3. The `window.__KONGGER_CONFIG` object in `<head>` sets:
   - `apiBase` — URL of kongger-api (default: `/api/v1`)
   - `appName` — Your brand name (default: `Kongger`)
   - `themeColour` — Primary colour hex (default: `#4a90d9`)

## White-Label / Rebrand

To resell as your own product, change these values in `index.html`:

```html
<script>
  window.__KONGGER_CONFIG = {
    apiBase: 'https://api.yourbrand.com/api/v1',
    appName: 'YourBrand',
    themeColour: '#your-colour',
  };
</script>
```

## File Structure

```
kongger-web/
├── index.html                  Entry point (landing page)
├── .env.example                Configuration template
├── js/
│   └── modules/
│       └── db-client.js        API client (Profile, Post, Page,
│                               Neighbour, Notification, Waitlist,
│                               Comment APIs)
└── README.md
```

## API Client

`js/modules/db-client.js` provides:
- In-memory cache with configurable TTL
- Debounced write queue (500ms default)
- Optimistic UI support (cache invalidation on writes)
- Auto-auth via `window.__KONGGER_CONFIG.authToken`

## Sellable As

| Package | Contents | For |
|---------|----------|-----|
| **kongger-web** (this) | HTML/JS frontend + db-client.js | Clients who need frontend template |
| **kongger-stack** | Both + Docker | Full-platform deployment |
