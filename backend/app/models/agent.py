"""Agent ORM model — represents a registered AI agent."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import Base


class Agent(Base):
    """An AI agent registered in the AI One platform."""

    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, default=22, nullable=False)
    role = Column(String(100), default="worker", nullable=False)
    status = Column(
        String(50),
        default="offline",
        nullable=False,
    )  # online, offline, provisioning, error
    api_key = Column(String(255), nullable=True)
    config = Column(JSONB, default=dict, nullable=True)
    last_heartbeat = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Agent id={self.id} name={self.name!r} status={self.status!r}>"
