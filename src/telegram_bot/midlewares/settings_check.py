from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from redis.asyncio import Redis
from aiogram.types import Message

from redis_controller import RedisController
from src.telegram_bot.resources.dto import UserSettingsDTO


class SettingsCheck(BaseMiddleware):
    def __init__(self, controller: RedisController) -> None:
        super().__init__()
        self._controller = controller

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if result := await self._controller.get_user_settings(event.from_user.id):
            data.update(self._get_data(result))
            return await handler(event, data)

        settings = UserSettingsDTO(False, 'Field-Tested', False)
        await self._controller.set_user_settings(event.from_user.id, settings)

        data.update(self._get_data(settings))
        return await handler(event, data)

    @staticmethod
    def _get_data(settings: UserSettingsDTO) -> Dict[str, Any]:
        return {
            'stattrak_setting': settings.stattrak,
            'quality_setting': settings.quality,
            'search_setting': settings.search
        }


