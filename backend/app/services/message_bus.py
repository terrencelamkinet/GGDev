"""Message Bus — Redis Pub/Sub interface for agent communication."""

import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.config import settings


class MessageBus:
    """Async Redis Pub/Sub message bus for agent events."""

    def __init__(self) -> None:
        self._redis: Optional[aioredis.Redis] = None
        self._pubsub: Optional[aioredis.client.PubSub] = None

    async def _get_redis(self) -> aioredis.Redis:
        """Lazy-init Redis connection."""
        if self._redis is None:
            self._redis = aioredis.from_url(
                settings.redis_url,
                decode_responses=True,
            )
        return self._redis

    async def publish(
        self, channel: str, message: dict[str, Any]
    ) -> int:
        """Publish a JSON message to a Redis channel.

        Args:
            channel: Redis channel name (e.g. "events").
            message: Dict to serialize as JSON.

        Returns:
            Number of subscribers that received the message.
        """
        redis = await self._get_redis()
        result = await redis.publish(channel, json.dumps(message))
        return result

    async def subscribe(
        self, channel: str
    ) -> aioredis.client.PubSub:
        """Subscribe to a Redis channel and return the PubSub object.

        Args:
            channel: Redis channel name.

        Returns:
            Redis PubSub object for iterating messages.
        """
        if self._pubsub is None:
            redis = await self._get_redis()
            self._pubsub = redis.pubsub()
        await self._pubsub.subscribe(channel)
        return self._pubsub

    async def close(self) -> None:
        """Close Redis connections."""
        if self._pubsub:
            await self._pubsub.close()
        if self._redis:
            await self._redis.close()
            self._redis = None


# Singleton instance
message_bus = MessageBus()
