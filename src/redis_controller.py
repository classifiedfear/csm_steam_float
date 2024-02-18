

from redis import asyncio as aioredis

from src.telegram_bot.resources.dto import UserSettingsDTO


class RedisController:
    def __init__(self, redis: aioredis.Redis) -> None:
        self._redis = redis

    async def get_user_settings(self, user_id: int) -> UserSettingsDTO:
        user_settings = await self._redis.hgetall(f'{user_id}_settings')
        return UserSettingsDTO(
            stattrak=True if user_settings[b'stattrak'].decode() == '1' else False,
            quality=user_settings[b'quality'].decode(),
            search=True if user_settings[b'search'].decode() == '1' else False
        )

    async def set_user_settings(self, user_id: int, settings: UserSettingsDTO) -> None:
        await self._redis.hset(f'{user_id}_settings', mapping={
            'stattrak': '1' if settings.stattrak else '0',
            'search': '1' if settings.search else '0',
            'quality': settings.quality,
        })

    async def set_quality(self, user_id: int, value: str) -> None:
        await self._redis.hset(f'{user_id}_settings', 'quality', value=value)

    async def set_stattrak(self, user_id: int, value: bool) -> None:
        await self._redis.hset(f'{user_id}_settings', 'stattrak', value='1' if value else '0')

    async def set_search(self, user_id: int, value: bool) -> None:
        await self._redis.hset(f'{user_id}_settings', 'search', value='1' if value else '0')