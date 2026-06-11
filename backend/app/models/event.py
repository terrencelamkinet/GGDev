"""Event ORM model — stores agent events and system events."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database import Base


class Event(Base):
    """An event in the AI One system — agent thoughts, status changes, errors."""

    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(100), nullable=False, index=True)
    source = Column(String(255), nullable=False)
    target = Column(String(255), nullable=True)
    payload = Column(JSONB, default=dict, nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Event id={self.id} type={self.type!r} source={self.source!r}>"
