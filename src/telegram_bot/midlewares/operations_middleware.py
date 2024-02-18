from typing import Callable, Dict, Any, Awaitable

from redis.asyncio import Redis
from aiogram import BaseMiddleware
from aiogram.types import Message

from redis_controller import RedisController


class GetterDefaultSettings(BaseMiddleware):
    def __init__(self, redis_controller: RedisController) -> None:
        super().__init__()
        self._controller = redis_controller

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_settings = await self._controller.get_user_settings(event.from_user.id)
        data['stattrak'] = user_settings.stattrak
        data['quality'] = user_settings.quality
        data['search'] = user_settings.search
        return await handler(event, data)
