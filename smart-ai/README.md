***REMOVED*** Smart AI — Desktop Hermes Client

***REMOVED******REMOVED*** Architecture

```
Windows 11 Desktop                    Linux VPS (this machine)
┌──────────────────────┐          ┌────────────────────────┐
│  Smart AI App        │  HTTP    │  smart-ai-server       │
│  (Electron)          │◄───────►│  (FastAPI :8765)        │
│                      │  POST   │         │               │
│  • Chat UI           │  /chat  │  calls  │               │
│  • Voice input       │         │  LLM    │               │
│  • Quick note        │         │  API    │               │
│  • Recording         │         └────────┴───────────────┘
│  • 3D Diagram        │
│  • System status     │
└──────────────────────┘
```

***REMOVED******REMOVED*** Build Instructions (Windows 11)

***REMOVED******REMOVED******REMOVED*** Prerequisites
- Node.js v18+: https://nodejs.org/

***REMOVED******REMOVED******REMOVED*** Steps
```bash
tar xzf smart-ai.tar.gz
cd smart-ai
npm install
npm run build:win
```

Installer will be at `dist/SmartAI-Setup-1.0.0.exe`

***REMOVED******REMOVED******REMOVED*** Quick Dev Start
```bash
npm start
```

***REMOVED******REMOVED*** Controls
| Action | Method |
|--------|--------|
| Toggle overlay | `Ctrl+Alt+A` |
| Send chat | Type + Enter |
| Quick input | Bottom bar text field |
| Record voice | 🎤 button (saves to ~/.smart-ai/recordings/) |
| Switch tabs | Click tab buttons |

***REMOVED******REMOVED*** Configuration
Edit `~/.smart-ai/config.json` after first run:
- `server_url`: Smart AI server address (default: http://localhost:8765)
- `weather_api_key`: OpenWeatherMap API key (free tier)
- `telegram_token`/`telegram_chat_id`: Optional — direct Telegram integration

***REMOVED******REMOVED*** Tabs
| Tab | Function |
|-----|----------|
| 💬 Chat | Text conversation with Hermes AI |
| 🧠 Diagram | 3D mind map (standalone THREE.js) |
| 📝 Notes | Quick note-taking |
| 📋 Tasks | TODO |

***REMOVED******REMOVED*** Server
Server runs on port 8765 (separate from AI Central).
Start: `python3 server.py`
