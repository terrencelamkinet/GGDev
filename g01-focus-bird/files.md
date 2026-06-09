# G01 — Focus Bird File Inventory

## Project Roots

| Path | Description |
|------|-------------|
| `projects/ggdev-repo/focus-bird/` | v1.0 production game (legacy) |
| `projects/ggdev-repo/focus-bird-dev/` | v2.0 development game (active) |

## Source Files (via symlink/`code/`)

| File | Size | Purpose |
|------|------|---------|
| `code/focus_bird/game.html` | — | Main game canvas (v2.0) |
| `code/focus_bird/index.html` | — | v1.0 index |
| `code/focus_bird/mockup.html` | — | v1.0 mockup |
| `code/focus_bird/game.html.bak` | — | v1.0 game backup |
| `code/focus_bird/ngfw-quiz.html` | — | NGFW quiz (related) |
| `code/focus_bird/questions-ngfw.js` | — | NGFW quiz questions |
| `code/focus_bridge/brainlink_bridge.py` | 12KB | X1 bridge: BrainLink → WebSocket |
| `code/focus_bridge/brainlink_simulator.py` | — | BrainLink simulator for testing |
| `code/focus_bridge/agent_relay_server.py` | — | Relay server (legacy) |
| `code/focus_bridge/requirements.txt` | — | Python deps for bridge |
| `code/focus_bridge/config.txt` | — | Bridge config |
| `code/focus_bridge/start_bridge.bat` | — | Bridge startup (Windows) |
| `code/focus_bridge/setup_once.bat` | — | One-time setup (Windows) |
| `code/focus_bridge/brainlink-integration-spec.md` | — | BrainLink integration spec doc |
| `code/spec/focus-bird-v2-design-spec.md` | 24KB | v2.0 full design specification |

## Context & Metadata

| File | Purpose |
|------|---------|
| `CONTEXT.md` | Current project context (from focus-bird-dev, latest) |
| `README.md` | This file — project overview |

## Infrastructure (VM-side, not in repo)

| Path | Purpose |
|------|---------|
| `~/.hermes/scripts/brainlink_relay.py` | Relay server on GG-Fighter VM |
| `/etc/systemd/system/brainlink-relay.service` | Systemd service for relay |
| `/etc/systemd/system/cloudflared-focusbird.service` | Cloudflare tunnel service |
| `~/.cloudflared/` | Tunnel credentials & cert |
