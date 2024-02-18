from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.telegram_bot.db import Quality, Skin, Weapon, WeaponSkinQuality


class DbSkinUpdater:
    @staticmethod
    async def add_weapon(session_maker: async_sessionmaker, weapon_name: str) -> int:
        async with session_maker() as session:
            result = await DbSkinUpdater._add_model(session, Weapon, {'name': weapon_name})
            return result.id

    @staticmethod
    async def add_skin(session_maker: async_sessionmaker, skin_name: str, stattrak_existence: int = 0) -> int:
        async with session_maker() as session:
            result = await DbSkinUpdater._add_model(
                session, Skin, {'name': skin_name, 'stattrak': stattrak_existence}
            )
            return result.id

    @staticmethod
    async def add_quality(session_maker: async_sessionmaker, quality_tile: str) -> int:
        async with session_maker() as session:
            result = await DbSkinUpdater._add_model(session, Quality, {'title': quality_tile})
            return result.id

    @staticmethod
    async def _add_model(session: AsyncSession, model, attrs: Dict[str, Any]):
        stmt = insert(model).values(attrs).returning(model)
        result_model = await session.scalar(stmt)
        await session.commit()
        return result_model

    @staticmethod
    async def get_skin(session_maker: async_sessionmaker, id: int):
        async with session_maker() as session:
            return await DbSkinUpdater._get_model(session, Skin, id)

    @staticmethod
    async def get_weapon(session_maker: async_sessionmaker, id: int):
        async with session_maker() as session:
            return await DbSkinUpdater._get_model(session, Weapon, id)

    @staticmethod
    async def get_quality(session_maker: async_sessionmaker, id: int):
        async with session_maker() as session:
            return await DbSkinUpdater._get_model(session, Quality, id)

    @staticmethod
    async def _get_model(session: AsyncSession, model, id: int):
        stmt = select(model).where(model.id == id)
        return await session.scalar(stmt)

    @staticmethod
    async def get_skin_id_by_name(session_maker: async_sessionmaker, name: str):
        async with session_maker() as session:
            stmt = select(Skin.id).where(Skin.name == name)
            result = await session.execute(stmt)
            return result.scalar()

    @staticmethod
    async def get_quality_id_by_title(session_maker: async_sessionmaker, title: str):
        async with session_maker() as session:
            stmt = select(Quality.id).where(Quality.title == title)
            result = await session.execute(stmt)
            return result.scalar()


    @staticmethod
    async def add_associations_between_weapon_skin_quality(
            session_maker: async_sessionmaker, weapon_id: int, skin_id: int, quality_id: int
    ):
        async with session_maker() as session:
            weapon = await DbSkinUpdater._get_model(session, Weapon, weapon_id)
            skin = await DbSkinUpdater._get_model(session, Skin, skin_id)
            quality = await DbSkinUpdater._get_model(session, Quality, quality_id)
            assoc = WeaponSkinQuality(weapon=weapon, skin=skin, quality=quality)
            session.add(assoc)
            await session.commit()

    @staticmethod
    async def get_skin_associations(session_maker: async_sessionmaker, skin_id: int, weapon_id: int, quality_id: int):
        async with session_maker() as session:
            stmt = (
                select(Skin.name, Weapon.name, Quality.title, Skin.stattrak)
                .join(Skin.w_s_q).join(WeaponSkinQuality.weapon)
                .join(WeaponSkinQuality.quality)
                .where(
                    WeaponSkinQuality.skin_id == skin_id,
                    WeaponSkinQuality.quality_id == quality_id,
                    WeaponSkinQuality.weapon_id == weapon_id
                ))
            result = await session.execute(stmt)
            return result.one_or_none()

    @staticmethod
    async def get_weapon_id_by_name(session_maker: async_sessionmaker, weapon_name: str):
        async with session_maker() as session:
            stmt = select(Weapon.id).where(Weapon.name == weapon_name)
            return await session.scalar(stmt)
