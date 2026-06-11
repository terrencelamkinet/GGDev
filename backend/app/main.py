"""FastAPI application entry point for AI One platform."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, async_session_factory
from app.routers import agents, provision, ws


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown events."""
    # Startup: verify DB connection
    async with engine.begin() as conn:
        from sqlalchemy import text
        await conn.execute(text("SELECT 1"))
        print("[AI One] Database connection verified.")

    yield

    # Shutdown: dispose engine
    await engine.dispose()
    print("[AI One] Engine disposed.")


app = FastAPI(
    title="AI One API",
    description="Central AI Agent Management Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(provision.router, prefix="/api/provision", tags=["Provision"])
app.include_router(ws.router, prefix="/ws", tags=["WebSocket"])


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "ai-one",
        "version": "0.1.0",
    }
