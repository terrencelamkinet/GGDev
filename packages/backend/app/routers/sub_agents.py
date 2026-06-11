"""
Sub-Agent Config API Router
============================
CRUD endpoints for sub-agent configuration (stored in SQLite/PostgreSQL
with Fernet encryption for sensitive fields).
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.sub_agent import SubAgentConfig
from app.services.encryption import encrypt, decrypt
from app.services.agent_discovery import _fetch_via_ssh_tunnel

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────

class SubAgentCreate(BaseModel):
    id: str
    name: str
    display_name: Optional[str] = None
    host: str
    ssh_port: int = 22
    ssh_username: str = "airoot"
    auth_type: str = "key"
    credential: Optional[str] = None
    exporter_port: int = 5004
    description: Optional[str] = ""
    is_active: bool = True


class SubAgentUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    host: Optional[str] = None
    ssh_port: Optional[int] = None
    ssh_username: Optional[str] = None
    auth_type: Optional[str] = None
    credential: Optional[str] = None
    exporter_port: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SubAgentResponse(BaseModel):
    id: str
    name: str
    display_name: Optional[str] = None
    host: str
    ssh_port: int
    ssh_username: Optional[str] = None
    auth_type: str
    credential: Optional[str] = None
    exporter_port: int
    description: Optional[str] = ""
    is_active: bool
    last_seen: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Helper: decrypt credential before response ────────────

def _decrypt_for_response(config: SubAgentConfig) -> dict:
    """Convert ORM model to dict, decrypting credential."""
    data = {
        "id": config.id,
        "name": config.name,
        "display_name": config.display_name,
        "host": config.host,
        "ssh_port": config.ssh_port,
        "ssh_username": config.ssh_username,
        "auth_type": config.auth_type,
        "credential": decrypt(config.credential) if config.credential else None,
        "exporter_port": config.exporter_port,
        "description": config.description or "",
        "is_active": config.is_active,
        "last_seen": config.last_seen,
        "created_at": config.created_at,
        "updated_at": config.updated_at,
    }
    return data


# ── Endpoints ─────────────────────────────────────────────

@router.get("/configs", response_model=list[SubAgentResponse])
async def list_configs(session: AsyncSession = Depends(get_session)):
    """List all sub-agent configs."""
    result = await session.execute(
        select(SubAgentConfig).order_by(SubAgentConfig.created_at.desc())
    )
    configs = list(result.scalars().all())
    # Decrypt credentials for response
    return [_decrypt_for_response(c) for c in configs]


@router.get("/configs/{agent_id}", response_model=SubAgentResponse)
async def get_config(agent_id: str, session: AsyncSession = Depends(get_session)):
    """Get a single sub-agent config."""
    result = await session.execute(
        select(SubAgentConfig).where(SubAgentConfig.id == agent_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail=f"Config '{agent_id}' not found")
    return _decrypt_for_response(config)


@router.put("/configs/{agent_id}", response_model=SubAgentResponse)
async def update_config(agent_id: str, data: SubAgentUpdate,
                        session: AsyncSession = Depends(get_session)):
    """Update a sub-agent config (edit display name, host, credentials, etc.)."""
    result = await session.execute(
        select(SubAgentConfig).where(SubAgentConfig.id == agent_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail=f"Config '{agent_id}' not found")

    update_data = data.model_dump(exclude_unset=True)

    # Encrypt credential if provided
    if "credential" in update_data and update_data["credential"]:
        update_data["credential"] = encrypt(update_data["credential"])
    elif "credential" in update_data:
        update_data["credential"] = ""

    for key, value in update_data.items():
        setattr(config, key, value)

    config.updated_at = datetime.utcnow()
    await session.flush()
    await session.refresh(config)
    return _decrypt_for_response(config)


@router.delete("/configs/{agent_id}", status_code=204)
async def delete_config(agent_id: str, session: AsyncSession = Depends(get_session)):
    """Delete a sub-agent config from the database."""
    result = await session.execute(
        select(SubAgentConfig).where(SubAgentConfig.id == agent_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail=f"Config '{agent_id}' not found")
    await session.delete(config)
    await session.flush()


@router.get("/exporter/{agent_id}")
async def get_agent_exporter_data(agent_id: str, session: AsyncSession = Depends(get_session)):
    """Fetch ALL exporter data from a sub-agent via SSH tunnel."""
    from app.services.agent_discovery import _fetch_via_ssh_tunnel

    result = await session.execute(
        select(SubAgentConfig).where(SubAgentConfig.id == agent_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(404, f"Agent '{agent_id}' not found")

    # Use capabilities endpoint (returns skills, tools, mcp, system, memory, cron)
    # + agent-info separately — only 2 tunnel calls instead of 7
    endpoints = ["agent-info", "capabilities"]
    data = {}
    for ep in endpoints:
        result_data = _fetch_via_ssh_tunnel(config.host, config.exporter_port, f"/api/v1/{ep}")
        if result_data:
            data[ep.replace("-", "_")] = result_data
        else:
            data[ep.replace("-", "_")] = None

    return {"agent_id": agent_id, "data": data}
