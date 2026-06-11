"""Agent Registry — CRUD operations for agent storage."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent


class AgentRegistry:
    """Service for managing agent records in the database."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Retrieve an agent by its UUID."""
        result = await self.session.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        return result.scalar_one_or_none()

    async def get_by_host(self, host: str) -> Optional[Agent]:
        """Retrieve an agent by its host address."""
        result = await self.session.execute(
            select(Agent).where(Agent.host == host)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        name: str,
        host: str,
        role: str = "worker",
        port: int = 22,
        config: Optional[dict] = None,
    ) -> Agent:
        """Create and persist a new agent record."""
        agent = Agent(
            name=name,
            host=host,
            port=port,
            role=role,
            config=config or {},
        )
        self.session.add(agent)
        await self.session.flush()
        await self.session.refresh(agent)
        return agent

    async def update_status(
        self, agent_id: UUID, status: str
    ) -> Optional[Agent]:
        """Update an agent's status."""
        agent = await self.get_by_id(agent_id)
        if agent:
            agent.status = status
            await self.session.flush()
            await self.session.refresh(agent)
        return agent

    async def delete(self, agent_id: UUID) -> bool:
        """Delete an agent record. Returns True if deleted."""
        agent = await self.get_by_id(agent_id)
        if agent:
            await self.session.delete(agent)
            await self.session.flush()
            return True
        return False
