# NEXUS CRM — Ivory Edition

Single-file HTML/CSS/JS CRM app combining:
- Full sidebar + topbar app shell with light/dark toggle (default: ivory/cream light theme)
- Dashboard with Focus Timer, Today's Tasks/Meetings, weekly calendar grid with a LIVE "now" time indicator line, Activity chart, Deals donut, Reminders
- Hash-based routing across all modules: Dashboard, Contacts (+detail), Companies (+detail), Deals Kanban (+detail), Tasks, Touchpoints, NameCards, Settings

## Usage
Open `nexus-crm-app.html` directly in any modern browser. No build step or server required.

## Notes
- Sample data is embedded in the `<script>` block (const D) — swap with real API calls per the NEXUS-SaaS-Build-Guide.md contract.
- The "now" line on the dashboard weekly grid auto-updates every 60 seconds based on the browser's local time.
