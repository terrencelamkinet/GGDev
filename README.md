# AI One 🦾

**The operating system for AI agents.**

Deploy, manage, and orchestrate AI agents across any server with one click. Enter host + username + password — AI One auto-SSH, auto-install, auto-connect.

## Quick Start

```bash
docker compose up -d
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

## Architecture

```
User → AI One Dashboard
         ├── Agent Registry (PostgreSQL)
         ├── Provisioner (Paramiko SSH → auto-install)
         ├── Message Bus (Redis Pub/Sub)
         └── Real-Time Gateway (WebSocket)
```

## Projects Structure

```
g04-ai-one/
├── PRD.md                 # Product requirements
├── ARCHITECTURE.md        # System design
├── backend/               # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── main.py        # Entry point
│   │   ├── models/        # ORM models
│   │   ├── routers/       # API endpoints
│   │   └── services/      # Business logic
│   └── alembic/           # DB migrations
├── frontend/              # React 19 + TypeScript + Tailwind
│   └── src/
│       ├── pages/         # Dashboard, Agents, Provision, Detail
│       └── components/    # AgentCard, AgentStream, ProvisionForm
├── docker-compose.yml
└── README.md
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13 + FastAPI + SQLAlchemy 2.0 |
| Frontend | TypeScript + React 19 + Tailwind v4 + shadcn/ui |
| Database | PostgreSQL 17 |
| Cache/Bus | Redis 8 |
| Real-Time | WebSocket |
| Provision | Paramiko SSH |
| Deploy | Docker Compose |
