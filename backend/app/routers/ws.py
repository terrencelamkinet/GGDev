"""WebSocket endpoint for real-time agent event streaming."""

import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.message_bus import message_bus

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket connection."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Send a JSON message to all connected clients."""
        dead: list[WebSocket] = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                dead.append(connection)
        for conn in dead:
            self.active_connections.remove(conn)


manager = ConnectionManager()


@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time agent event streaming.

    Clients connect here and receive JSON events pushed from the backend.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive — receive pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def broadcast_event(
    event_type: str,
    source: str,
    payload: dict[str, Any] | None = None,
    target: str | None = None,
) -> None:
    """Broadcast an event to all connected WebSocket clients."""
    message = {
        "type": event_type,
        "source": source,
        "target": target,
        "payload": payload or {},
    }
    await manager.broadcast(message)

    # Also publish to Redis
    try:
        await message_bus.publish("events", message)
    except Exception:
        pass  # Redis may not be available
