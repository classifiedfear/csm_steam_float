from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from redis import asyncio as aioredis


from src.telegram_bot.db import user_queries


class RegisterCheck(BaseMiddleware):
    def __init__(self, redis: aioredis) -> None:
        super().__init__()
        self.redis = redis

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        #await self.redis.delete(str(event.from_user.id))
        if await self.redis.get(name=str(event.from_user.id)):
            return await handler(event, data)
        if not await user_queries.UserQueries.is_user_exists(event.from_user.id):
            await user_queries.UserQueries.add_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.full_name
            )
            await self.redis.set(name=str(event.from_user.id), value=1)
        return await handler(event, data)
