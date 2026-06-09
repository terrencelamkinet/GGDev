"""Provisioning API endpoint — one-click SSH deploy."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.agent import Agent
from app.models.deployment import Deployment
from app.schemas.agent import ProvisionRequest, ProvisionResponse
from app.services.provisioner import provision_agent

router = APIRouter()


@router.post("/", response_model=ProvisionResponse)
async def provision(
    req: ProvisionRequest,
    session: AsyncSession = Depends(get_session),
) -> ProvisionResponse:
    """One-click provision: SSH into server, install agent, register."""
    # Generate a temporary agent record
    agent_name = req.name or f"agent-{uuid.uuid4().hex[:8]}"

    agent = Agent(
        name=agent_name,
        host=req.host,
        port=req.port,
        role=req.role,
        status="provisioning",
    )
    session.add(agent)
    await session.flush()
    await session.refresh(agent)

    # Create deployment record
    deployment = Deployment(
        agent_id=agent.id,
        host=req.host,
        status="running",
    )
    session.add(deployment)
    await session.flush()
    await session.refresh(deployment)

    try:
        # Run provisioner
        result = await provision_agent(
            host=req.host,
            port=req.port,
            username=req.username,
            password=req.password,
            agent_id=agent.id,
            agent_name=agent_name,
            role=req.role,
        )

        # Update agent on success
        agent.status = "online"
        agent.api_key = result.get("api_key")
        agent.config = result.get("config", {})

        deployment.status = "success"
        deployment.log = result.get("log", "Provisioning completed successfully.")

        await session.flush()

        return ProvisionResponse(
            deployment_id=deployment.id,
            agent_id=agent.id,
            status="success",
            message=f"Agent {agent_name} deployed successfully on {req.host}",
        )

    except Exception as exc:
        # Mark as failed
        agent.status = "error"
        deployment.status = "failed"
        deployment.log = f"Provisioning failed: {str(exc)}"
        await session.flush()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Provisioning failed: {str(exc)}",
        )
