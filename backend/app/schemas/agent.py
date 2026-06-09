"""Pydantic schemas for Agent API operations."""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    """Schema for creating a new agent."""

    name: str = Field(..., min_length=1, max_length=255, description="Agent name")
    host: str = Field(..., min_length=1, max_length=255, description="Server hostname or IP")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port")
    role: str = Field(default="worker", max_length=100, description="Agent role")
    config: dict[str, Any] = Field(default_factory=dict, description="Agent configuration JSON")


class AgentUpdate(BaseModel):
    """Schema for updating an existing agent."""

    name: Optional[str] = Field(default=None, max_length=255)
    role: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default=None, max_length=50)
    config: Optional[dict[str, Any]] = None


class AgentResponse(BaseModel):
    """Schema for agent response data."""

    id: UUID
    name: str
    host: str
    port: int
    role: str
    status: str
    api_key: Optional[str] = None
    config: Optional[dict[str, Any]] = None
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProvisionRequest(BaseModel):
    """Schema for one-click provision request."""

    host: str = Field(..., min_length=1, max_length=255, description="Server hostname or IP")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port")
    username: str = Field(..., min_length=1, max_length=255, description="SSH username")
    password: str = Field(..., min_length=1, max_length=4096, description="SSH password")
    name: Optional[str] = Field(default=None, max_length=255, description="Agent name (auto-generated if empty)")
    role: str = Field(default="worker", max_length=100, description="Agent role")


class ProvisionResponse(BaseModel):
    """Schema for provision response."""

    deployment_id: UUID
    agent_id: Optional[UUID] = None
    status: str
    message: str
