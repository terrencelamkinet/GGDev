# KONGGER API

**Social Platform Backend** — a sellable, white-label API product.

A PostgreSQL-backed REST API for social networking platforms. Includes user authentication, profile management, social feed, canvas pages, neighbour graph, virtual gifts, and waitlist management.

## Product Features

- **Modular API** — 30+ REST endpoints across 7 domains
- **Row-Level Security** — data isolation baked into the database
- **Cursor Pagination** — performant infinite scroll on all list endpoints
- **Optimistic UI Support** — client-side caching + debounced writes
- **Auto-scaling** — connection pooling, rate limiting, materialized views

## Quick Start

```bash
npm install
cp .env.example .env   # Edit PG_CONNECTION_STRING and JWT_SECRET
npm run db:init         # Creates all tables, indexes, RLS policies
npm run db:seed         # Optional: development seed data
npm start               # API starts on PORT (default 3001)
```

## Sellable As

| Package | Contents | For |
|---------|----------|-----|
| **kongger-api** (this) | Node.js API + PostgreSQL schema | Clients who need backend-only |
| **kongger-web** | HTML/JS frontend + db-client.js | Clients who need frontend template |
| **kongger-stack** | Both + Docker Compose | Full-platform deployment |

## API Endpoints

```
GET    /health                          Health check
POST   /api/v1/auth/register             Register new user
POST   /api/v1/auth/login                Login

GET    /api/v1/profiles/me               Get own profile
GET    /api/v1/profiles/:handle          Get profile by handle
PATCH  /api/v1/profiles/me               Update profile
POST   /api/v1/profiles/:id/visit        Log profile visit
GET    /api/v1/profiles/:id/visitors     Get visitor count

GET    /api/v1/posts/feed                Neighbour feed (cursor paginated)
GET    /api/v1/posts?author=:id          User's posts
GET    /api/v1/posts/:id                 Single post
POST   /api/v1/posts                     Create post
PATCH  /api/v1/posts/:id                 Update post
DELETE /api/v1/posts/:id                 Delete post
POST   /api/v1/posts/:id/like            Like post
DELETE /api/v1/posts/:id/like            Unlike post

GET    /api/v1/posts/:postId/comments     Comments on post (cursor paginated)
POST   /api/v1/posts/:postId/comments     Add comment
DELETE /api/v1/comments/:id               Soft-delete comment

GET    /api/v1/pages?owner=:id           User's published pages
GET    /api/v1/pages/:ownerId/:slug      Single page with sections
POST   /api/v1/pages                     Create page
PATCH  /api/v1/pages/:id/layout          Save page layout (debounced)
PATCH  /api/v1/pages/:id/sections        Save page sections
DELETE /api/v1/pages/:id                 Delete page

GET    /api/v1/neighbours                List neighbours
POST   /api/v1/neighbours/:userId        Send neighbour request
PATCH  /api/v1/neighbours/:id/accept     Accept neighbour request

GET    /api/v1/notifications             List notifications
PATCH  /api/v1/notifications/read-all    Mark all read

POST   /api/v1/waitlist                  Join waitlist
```

## Configuration (all via `.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PG_CONNECTION_STRING` | ✅ | — | PostgreSQL connection string |
| `JWT_SECRET` | ✅ | — | JWT signing secret (min 32 chars) |
| `PORT` | | 3001 | HTTP listen port |
| `ALLOWED_ORIGIN` | | `*` | CORS allowed origins |

## Deployment

```bash
# Standalone
node server.js

# Docker
docker compose up -d

# Production (nginx reverse proxy)
# See nginx.conf for reference
```

## Migration Path

- **App**: Replace `db-client.js` with Flutter Repository / React Native Zustand
- **Database**: Schema is Supabase-compatible. Replace direct PG with `supabase.from().select()`
- **Auth**: Swap JWT for Supabase Auth / Clerk / Auth0 with minimal SQL changes
