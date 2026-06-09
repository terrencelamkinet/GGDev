***REMOVED*** OpenCode MCP Configuration

This directory contains MCP (Model Context Protocol) server configurations.

***REMOVED******REMOVED*** Available MCP Servers

***REMOVED******REMOVED******REMOVED*** Local MCP
| Server | Description | Command |
|--------|------------|---------|
| shadcn/ui | Generate shadcn/ui components | `npx shadcn@latest add` |

***REMOVED******REMOVED******REMOVED*** Remote MCP
| Server | Description | Endpoint |
|--------|------------|----------|
| Perplexity | Research + web-grounded reasoning | http://localhost:3100 |
| Notion | Task context from Notion | http://localhost:3101 |
| Google Maps | Calendar/contacts context | http://localhost:3102 |
| HK Transport | HK transport ETA | http://localhost:3103 |
| Design Lang | Design tokens & components | http://localhost:3104 |

***REMOVED******REMOVED*** How to Add MCP Servers

***REMOVED******REMOVED******REMOVED*** Option 1: Via opencode.json
Edit `~/.config/opencode/opencode.json` and add to `mcpServers`:

```json
"mcpServers": {
  "my-server": {
    "type": "local",
    "command": "npx",
    "args": ["my-mcp-server"]
  }
}
```

***REMOVED******REMOVED******REMOVED*** Option 2: Via OpenCode CLI
```bash
opencode mcp add --name my-server --command "npx my-mcp-server"
```

***REMOVED******REMOVED******REMOVED*** Option 3: Via OpenCode chat
```
/mcp add my-server
```

***REMOVED******REMOVED*** MCP Server Definitions

***REMOVED******REMOVED******REMOVED*** shadcn/ui (Local)
Component generator for React/Tailwind projects.
```json
{
  "type": "local",
  "command": "npx",
  "args": ["shadcn@latest", "add"]
}
```

***REMOVED******REMOVED******REMOVED*** Perplexity (Remote)
Web-grounded research and reasoning.
```json
{
  "type": "remote",
  "url": "http://localhost:3100"
}
```
