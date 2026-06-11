***REMOVED*** AI One 🦾

**The operating system for AI agents.**

Deploy, manage, and orchestrate AI agents across any server with one click. Enter host + username + password — AI One auto-SSH, auto-install, auto-connect.

***REMOVED******REMOVED*** Quick Start

```bash
docker compose up -d
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

***REMOVED******REMOVED*** Architecture

```
User → AI One Dashboard
         ├── Agent Registry (PostgreSQL)
         ├── Provisioner (Paramiko SSH → auto-install)
         ├── Message Bus (Redis Pub/Sub)
         └── Real-Time Gateway (WebSocket)
```

***REMOVED******REMOVED*** Projects Structure

```
g04-ai-one/
├── PRD.md                 ***REMOVED*** Product requirements
├── ARCHITECTURE.md        ***REMOVED*** System design
├── backend/               ***REMOVED*** FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── main.py        ***REMOVED*** Entry point
│   │   ├── models/        ***REMOVED*** ORM models
│   │   ├── routers/       ***REMOVED*** API endpoints
│   │   └── services/      ***REMOVED*** Business logic
│   └── alembic/           ***REMOVED*** DB migrations
├── frontend/              ***REMOVED*** React 19 + TypeScript + Tailwind
│   └── src/
│       ├── pages/         ***REMOVED*** Dashboard, Agents, Provision, Detail
│       └── components/    ***REMOVED*** AgentCard, AgentStream, ProvisionForm
├── docker-compose.yml
└── README.md
```

***REMOVED******REMOVED*** Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13 + FastAPI + SQLAlchemy 2.0 |
| Frontend | TypeScript + React 19 + Tailwind v4 + shadcn/ui |
| Database | PostgreSQL 17 |
| Cache/Bus | Redis 8 |
| Real-Time | WebSocket |
| Provision | Paramiko SSH |
| Deploy | Docker Compose |
