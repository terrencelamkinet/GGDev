***REMOVED*** NEXUS CRM — White Edition + Projects, Sales & Integrations

Single-file HTML/CSS/JS CRM app.

***REMOVED******REMOVED*** What's new in this version
- Settings page now has working sub-tabs via hash routing: `***REMOVED***settings/profile`, `***REMOVED***settings/team`, `***REMOVED***settings/integrations`, `***REMOVED***settings/billing`
- **Integrations sub-page** redesigned to mirror real-world API integration management UIs (Zapier/Notion/Vercel style):
  - Summary stat chips: total integrations, live count, pending/attention count, planned/not-started count
  - Grouped sections: Live & Running / In Progress-Pending / Future (Design01-Design02 SaaS)
  - Each integration rendered as a connection card: icon, name, status pill (color-coded dot: green=live, amber=pending, gold=partial, red=needs fix, blue=planned, gray=off), detail description, last-sync/meta line, and contextual actions (Configure/Disconnect, Resume/Details, Fix Now/Logs, View Preview, Connect)
  - Data reflects your actual integration status report: Notion CRM Sync, Google Calendar, PostgreSQL Task Hub, C1-C9 automation modules, Name Card OCR, Entity Matcher, SaaS frontends, Backend API, Multi-Tenant Auth, Billing, Real-time PG Sync
  - "+ Add Integration" CTA for connecting new services via API key/OAuth/webhook

***REMOVED******REMOVED*** Usage
Open `nexus-crm-app-white.html` directly in any modern browser. No build step required.

***REMOVED******REMOVED*** Routes
`***REMOVED***dashboard` `***REMOVED***contacts` `***REMOVED***contact-detail/:id` `***REMOVED***companies` `***REMOVED***company-detail/:id` `***REMOVED***deals` `***REMOVED***deal-detail`
`***REMOVED***projects` `***REMOVED***project-detail/:id` `***REMOVED***team` `***REMOVED***team-detail/:id` `***REMOVED***sales-dashboard`
`***REMOVED***tasks` `***REMOVED***touchpoints` `***REMOVED***namecards`
`***REMOVED***settings/profile` `***REMOVED***settings/team` `***REMOVED***settings/integrations` `***REMOVED***settings/billing`
