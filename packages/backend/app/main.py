"""AI Central Backend — FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from app.config import settings
from app.database import engine
from app.routers import agents, provision, ws, events, cronjobs, skills, mcp, apis, logs, upgrades, stats, install, sub_agents
from app.services.agent_discovery import discover as discover_agents


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown."""
    # Startup: verify DB connection & auto-create tables
    try:
        async with engine.begin() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
            print("[AI Central] Database connection verified.")
        # Auto-create tables (safe for SQLite, idempotent for PostgreSQL)
        from app.database import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("[AI Central] Database tables ensured.")
    except Exception as e:
        print(f"[AI Central] Database connection failed: {e}")
        print("[AI Central] Running without database — some features will be unavailable.")

    yield

    # Shutdown
    await engine.dispose()
    print("[AI Central] Engine disposed.")


app = FastAPI(
    title="AI Central API",
    description="AI Central — AI Upgrade Management Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers — app-level routes first (before wildcard router paths)


@app.get("/api/agents/discovery")
def agents_discovery():
    """Dynamically discover orchestrator + sub-agents."""
    return discover_agents()


app.include_router(sub_agents.router, prefix="/api/agents", tags=["Sub-Agent Configs"])
app.include_router(install.router, prefix="/api/agents", tags=["Agent Install"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(provision.router, prefix="/api/provision", tags=["Provision"])
app.include_router(ws.router, prefix="/ws", tags=["WebSocket"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(cronjobs.router, prefix="/api/cronjobs", tags=["Cron Jobs"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(mcp.router, prefix="/api/mcp", tags=["MCP Servers"])
app.include_router(apis.router, prefix="/api/apis", tags=["Connected APIs"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])
app.include_router(upgrades.router, prefix="/api/upgrades", tags=["Upgrades"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])

@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "ai-central", "version": "0.1.0"}


@app.get("/api/endpoints")
async def root():
    return {
        "service": "AI Central API",
        "version": "0.1.0",
        "endpoints": {
            "agents": "/api/agents",
            "provision": "/api/provision",
            "events": "/api/events",
            "cronjobs": "/api/cronjobs",
            "skills": "/api/skills",
            "mcp": "/api/mcp",
            "apis": "/api/apis",
            "logs": "/api/logs",
            "upgrades": "/api/upgrades",
            "stats": "/api/stats",
            "discovery": "/api/agents/discovery",
            "exporter": "/api/agents/exporter/{agent_id}",
            "test-connection": "/api/agents/test-connection",
            "install": "/api/agents/install",
            "health": "/health",
            "websocket": "/ws",
        },
    }


# Serve static frontend files (must be last — after all API routes)
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ai-central"
if FRONTEND_DIR.exists():
    from fastapi.responses import FileResponse, RedirectResponse, Response
    
    # Middleware to add cache-busting headers on ALL responses
    @app.middleware("http")
    async def add_cache_headers(request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Clear-Site-Data"] = '"cache","cookies","storage"'
        return response
    
    # Mount assets directory first (before catch-all routes)
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")
    
    # Service worker kill-switches — neutralize any old Next.js service workers
    @app.get("/sw.js", include_in_schema=False)
    @app.get("/service-worker.js", include_in_schema=False)
    async def service_worker_kill():
        js = (
            "self.addEventListener('install',function(){self.skipWaiting()});"
            "self.addEventListener('activate',function(e){"
            "e.waitUntil("
            "caches.keys().then(function(n){return Promise.all(n.map(function(k){return caches.delete(k)}))})"
            ".then(function(){return self.clients.matchAll()})"
            ".then(function(c){c.forEach(function(cl){cl.postMessage('reload')})})"
            ")"
            "});"
        )
        return Response(content=js, media_type="application/javascript")

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    # Catch old Next.js paths and browser cache ghosts
    # When the user's browser loads cached Next.js HTML, it tries to fetch
    # /_next/static/chunks/*.js as scripts. A 307 redirect to HTML causes
    # JS parse errors. Instead, we return valid JavaScript that forces a
    # hard page reload to the root with cache busting.
    @app.get("/_next/{rest:path}", include_in_schema=False)
    async def nextjs_catch(rest: str):
        js = (
            ";(function(){"
            "try{"
            "if('caches' in window){caches.keys().then(function(n){"
            "n.forEach(function(k){caches.delete(k)})"
            "})}"
            "}catch(e){}"
            "window.location.href='/?cb='+Date.now()+'&ts='+Math.random().toString(36).slice(2)"
            "})();"
        )
        from fastapi.responses import Response
        resp = Response(content=js, media_type="application/javascript")
        return resp

    @app.get("/{path:path}", include_in_schema=False)
    async def serve_static(path: str):
        file_path = FRONTEND_DIR / path
        if file_path.exists() and file_path.is_file():
            if path.startswith("assets/"):
                return FileResponse(str(file_path))
            return FileResponse(str(file_path))
        html_path = FRONTEND_DIR / f"{path}.html"
        if html_path.exists():
            return FileResponse(str(html_path))
        return FileResponse(str(FRONTEND_DIR / "index.html"))
