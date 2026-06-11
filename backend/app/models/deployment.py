"""Deployment ORM model — tracks SSH provisioning attempts."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Deployment(Base):
    """A deployment record tracking SSH provisioning of an agent."""

    __tablename__ = "deployments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=True
    )
    host = Column(String(255), nullable=False)
    status = Column(
        String(50), default="pending", nullable=False
    )  # pending, running, success, failed
    log = Column(Text, default="", nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Deployment id={self.id} host={self.host!r} status={self.status!r}>"
