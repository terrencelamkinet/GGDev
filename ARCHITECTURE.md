# AI One — System Architecture

## Overview

AI One is a centralized AI Agent management platform. Users provide server credentials, and the system auto-provisions AI agents via SSH, registers them in a central registry, and enables real-time monitoring via WebSocket.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Users / Browser                                │
│                    (React 19 + Tailwind v4)                             │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             │ HTTPS / WS
                             │
┌────────────────────────────▼────────────────────────────────────────────┐
│                         FastAPI Backend                                  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  /api/agents │  │ /api/provision│  │  /ws/stream  │  │ Middleware  │  │
│  │   Router     │  │   Router     │  │  WebSocket   │  │ (CORS,JWT) │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └────────────┘  │
│         │                 │                 │                           │
│  ┌──────▼─────────────────▼─────────────────▼──────────────────────┐   │
│  │                     Service Layer                                 │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐      │   │
│  │  │   Registry     │  │  Provisioner   │  │  Message Bus   │      │   │
│  │  │  (CRUD Agents) │  │ (Paramiko SSH) │  │(Redis Pub/Sub) │      │   │
│  │  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘      │   │
│  └──────────┼──────────────────┼──────────────────┼──────────────────┘   │
└─────────────┼──────────────────┼──────────────────┼──────────────────────┘
              │                  │                  │
    ┌─────────▼─────┐   ┌───────▼───────┐   ┌─────▼──────┐
    │  PostgreSQL 17 │   │  Target       │   │  Redis 8   │
    │  (Persistent)  │   │  Servers      │   │  (Pub/Sub) │
    │                │   │  (SSH)        │   │            │
    │  - agents      │   │               │   │  - events  │
    │  - deployments │   │  docker pull  │   │  - status  │
    │  - events      │   │  agent image  │   │  - cache   │
    └────────────────┘   └───────────────┘   └────────────┘
```

## Component Details

### 1. Agent Registry (PostgreSQL)
Stores all registered agents and their metadata.

```
agents
├── id            UUID PRIMARY KEY
├── name          VARCHAR(255)
├── host          VARCHAR(255)
├── port          INTEGER (default 22)
├── role          VARCHAR(100)          -- e.g. "worker", "supervisor", "chat"
├── status        VARCHAR(50)           -- online, offline, provisioning, error
├── api_key       VARCHAR(255)
├── config        JSONB                 -- flexible agent configuration
├── last_heartbeat TIMESTAMP
├── created_at    TIMESTAMP
└── updated_at    TIMESTAMP
```

```
deployments
├── id            UUID PRIMARY KEY
├── agent_id      UUID FK → agents.id
├── host          VARCHAR(255)
├── status        VARCHAR(50)           -- pending, running, success, failed
├── log           TEXT
└── created_at    TIMESTAMP
```

```
events
├── id            UUID PRIMARY KEY
├── type          VARCHAR(100)          -- agent.thought, agent.status, agent.error
├── source        VARCHAR(255)          -- agent ID or "system"
├── target        VARCHAR(255)          -- optional, nullable
├── payload       JSONB
└── created_at    TIMESTAMP
```

### 2. Provisioner Engine (Paramiko SSH)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1. SSH into  │────▶│ 2. Detect OS │────▶│ 3. Install   │────▶│ 4. Pull/     │
│   Target     │     │              │     │   Docker     │     │  Deploy      │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
┌──────────────┐     ┌──────────────┐     ┌──────────────┐           │
│ 7. Register  │◀────│ 6. Health    │◀────│ 5. Generate  │◀──────────┘
│   in AI One  │     │   Check      │     │   Agent ID   │
│   Registry   │     │              │     │   + API Key  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 3. Message Bus (Redis Pub/Sub)

```
                ┌──────────────────────────┐
                │       Redis 8            │
                │                          │
                │  ┌─────────────────────┐ │
                │  │   channel: events   │ │
                │  │  (Pub/Sub)          │ │
                │  └─────────┬───────────┘ │
                └────────────┼─────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
         │ Backend │   │ Agent 1 │   │ Agent N │
         │ (Pub)   │   │(Pub/Sub)│   │(Pub/Sub)│
         └─────────┘   └─────────┘   └─────────┘
```

### 4. Real-Time Gateway (FastAPI WebSocket)

```
 Browser/Client              FastAPI                  Redis
     │                         │                       │
     │── WS /ws/stream ──────▶│                       │
     │                         │── SUB events ───────▶│
     │                         │◀─── messages ────────│
     │◀─── JSON frames ───────│                       │
     │                         │                       │
     │  { type: "agent.status",                         │
     │    payload: { id, status, uptime } }             │
```

## Data Flow

### Provisioning Flow
1. User submits host + user + password via `POST /api/provision`
2. Backend creates a `Deployment` record (status: pending)
3. Provisioner service opens SSH connection via Paramiko
4. Streams log output back to client via WebSocket
5. On success: agent container starts, agent registers via API
6. Deployment status → success, Agent status → online

### Event Flow
1. Any component publishes to Redis channel `events`
2. Backend subscribes and fans out to connected WebSocket clients
3. Events persisted to Postgres `events` table for history
4. Frontend updates dashboard in real-time

## Security
- SSH credentials transmitted in-memory only, never stored
- Agent API keys generated per deployment
- JWT authentication for API endpoints
- CORS restricted to frontend origin
- Redis password-protected
- PostgreSQL credentials via environment variables

## Scalability
- Stateless FastAPI backend → horizontal scaling behind reverse proxy
- Redis Pub/Sub decouples agents from backend
- PostgreSQL connection pooling via asyncpg
- Frontend is static files → served via CDN or Nginx
