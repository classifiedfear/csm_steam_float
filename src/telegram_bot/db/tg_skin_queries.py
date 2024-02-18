from typing import Tuple

from sqlalchemy import select, and_, Row, func
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.telegram_bot.db import Skin, Weapon, Quality, WeaponSkinQuality
from src.telegram_bot.db.skindatabase import SkinDatabase


class TGSkinQueries:
    @staticmethod
    async def get_random_weapon_from_db(session_maker: async_sessionmaker) -> Row[Tuple[str, str, str, int]] | None:
        async with session_maker() as session:
            stmt = (
               select(Skin.name, Weapon.name, Quality.title, Skin.stattrak)
               .join(Skin.w_s_q)
               .join(WeaponSkinQuality.weapon)
               .join(WeaponSkinQuality.quality)
               .order_by(func.random())
               .limit(1)
            )
            result = await session.execute(stmt)
            return result.one_or_none()

    @staticmethod
    async def get_skins_for_weapon(session_maker: async_sessionmaker, weapon_id: int):
        async with session_maker() as session:
            stmt = (
                select(Skin.name)
                .join(Skin.w_s_q)
                .join(WeaponSkinQuality.weapon)
                .where(Weapon.id == weapon_id)
                )
            result = await session.execute(stmt)
            return result.all()
