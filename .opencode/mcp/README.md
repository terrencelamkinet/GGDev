# OpenCode MCP Configuration

This directory contains MCP (Model Context Protocol) server configurations.

## Available MCP Servers

### Local MCP
| Server | Description | Command |
|--------|------------|---------|
| shadcn/ui | Generate shadcn/ui components | `npx shadcn@latest add` |

### Remote MCP
| Server | Description | Endpoint |
|--------|------------|----------|
| Perplexity | Research + web-grounded reasoning | http://localhost:3100 |
| Notion | Task context from Notion | http://localhost:3101 |
| Google Maps | Calendar/contacts context | http://localhost:3102 |
| HK Transport | HK transport ETA | http://localhost:3103 |
| Design Lang | Design tokens & components | http://localhost:3104 |

## How to Add MCP Servers

### Option 1: Via opencode.json
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

### Option 2: Via OpenCode CLI
```bash
opencode mcp add --name my-server --command "npx my-mcp-server"
```

### Option 3: Via OpenCode chat
```
/mcp add my-server
```

## MCP Server Definitions

### shadcn/ui (Local)
Component generator for React/Tailwind projects.
```json
{
  "type": "local",
  "command": "npx",
  "args": ["shadcn@latest", "add"]
}
```

### Perplexity (Remote)
Web-grounded research and reasoning.
```json
{
  "type": "remote",
  "url": "http://localhost:3100"
}
```
