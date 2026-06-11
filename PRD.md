# AI One — Product Requirements Document

## Product Name
**AI One** — *The operating system for AI agents.*

## Elevator Pitch
> The operating system for AI agents. Deploy, manage, and orchestrate AI agents across any server with one click.

## Core Problem
Setting up AI agents is hard. Each server requires:
- SSH access configuration
- Python + Docker installation
- Environment variables and config files
- API key provisioning
- Manual health checks and monitoring

AI One automates all of this. Give it a host, username, and password — it handles the rest.

## Target Users
- **Developers** who want to spin up AI agents across multiple servers
- **Tech teams** managing fleets of AI agents for automation, monitoring, or chatbots
- **AI enthusiasts** running personal AI infrastructure at home or in the cloud

## MVP Features

### 1. Agent Registry
- See all connected agents in a single dashboard
- Status indicators: online, offline, provisioning, error
- Uptime tracking and last-seen timestamps
- Agent role / type classification

### 2. One-Click Provision
- Form: host + username + password (or SSH key)
- Auto-SSH into the target server
- Detect OS and install dependencies (Docker, Python, etc.)
- Deploy agent container with unique ID + API key
- Register agent in the central registry
- Return real-time provisioning logs via WebSocket

### 3. Real-Time Monitoring
- WebSocket push of agent thoughts, status changes, and health
- Live log viewer per agent
- Agent heartbeat detection (missed heartbeat = alert)

### 4. Message Bus
- Agents communicate via central Redis Pub/Sub event system
- Publish events: `agent.thought`, `agent.status`, `agent.error`
- Subscribe to events from the dashboard
- Historical event log stored in PostgreSQL

### 5. Log Viewer
- Tail agent logs directly from the dashboard
- Search and filter by log level, timestamp, or keyword
- Persistent log storage for post-mortem analysis

## Tech Stack
| Component       | Technology                          |
|-----------------|-------------------------------------|
| Backend         | Python 3.12 + FastAPI               |
| Frontend        | React 19 + TypeScript               |
| Styling         | Tailwind CSS v4 + shadcn/ui         |
| Database        | PostgreSQL 17                       |
| Cache / Bus     | Redis 8                             |
| SSH Provisioner | Paramiko                            |
| Migrations      | Alembic                             |
| Containerization| Docker + Docker Compose             |
| ORM             | SQLAlchemy 2.0 (async)              |

## Monetization
| Tier    | Price   | Limits                  |
|---------|---------|-------------------------|
| Free    | $0      | Up to 3 agents          |
| Pro     | $19/mo  | Unlimited agents        |
| Team    | $49/mo  | Unlimited agents + SSO  |

## Success Metrics
- Time to deploy a new agent: **< 60 seconds**
- Dashboard load time: **< 2 seconds**
- WebSocket message latency: **< 100ms**
- Uptime: **99.9%**
