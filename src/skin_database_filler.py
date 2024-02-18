import asyncio
import os
from typing import Tuple
from sqlalchemy import URL

from src.csgo_database.services.csgo_database_service import SkinDatabaseService
from src.misc.dto import DBSkinFiller
from src.misc.response_getter import CommonRequestExecutor
from src.telegram_bot.db.db_updater import DbSkinUpdater


from src.database_filler.cs_wiki.services.cs_wiki_service import CsWikiService
from src.telegram_bot.db.skindatabase import SkinDatabase, Base
from src.telegram_bot.resources.constants.skin_const import Qualities


class DBFiller:
    def __init__(
            self, database: SkinDatabase, skin_db_service: SkinDatabaseService, wiki_service: CsWikiService
    ):
        self._database = database
        self._skin_cs_db_service = skin_db_service
        self._wiki_service = wiki_service
        self._skins = {}

    async def fill(self):
        tasks = []
        for quality in Qualities:
            await DbSkinUpdater.add_quality(self._database.get_session_maker(), quality.str)
        for weapon in await self._skin_cs_db_service.get_weapons():
            weapon_id = await DbSkinUpdater.add_weapon(self._database.get_session_maker(), weapon)
            self._skins[weapon_id] = await self._get_existence_skins_for(weapon)
            tasks.append(asyncio.create_task(self._fill_relations_to_skins(weapon_id)))
        await asyncio.gather(*tasks)

    async def _fill_relations_to_skins(self, weapon_id: int):
        for filler in self._skins[weapon_id]:
            if isinstance(filler, DBSkinFiller):
                skin_id = await self._add_skin_to_db_if_not_exists(filler.skin, filler.stattrak_existence)
                for quality in filler.qualities:
                    quality_id = await DbSkinUpdater.get_quality_id_by_title(self._database.get_session_maker(), quality)
                    await DbSkinUpdater.add_associations_between_weapon_skin_quality(
                        self._database.get_session_maker(),
                        weapon_id, skin_id, quality_id
                    )


    async def _get_existence_skins_for(self, weapon: str) -> Tuple[DBSkinFiller]:
        tasks = []
        skins = await self._skin_cs_db_service.get_skin_for_weapon(weapon)
        for skin in skins:
            task = asyncio.create_task(self._wiki_service.get_skin(weapon, skin))
            tasks.append(task)
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def _add_skin_to_db_if_not_exists(self, skin: str, stattrak_existence: int = 0) -> None:
        if not (skin_id := await DbSkinUpdater.get_skin_id_by_name(
                self._database.get_session_maker(), skin)):
            skin_id = await DbSkinUpdater.add_skin(self._database.get_session_maker(), skin, stattrak_existence)
        return skin_id

    async def _add_quality_to_db_if_not_exists(self, quality: str) -> None:
        if not (quality_id := await DbSkinUpdater.get_quality_id_by_title(
                self._database.get_session_maker(), quality)):
            quality_id = await DbSkinUpdater.add_quality(self._database.get_session_maker(), quality)
        return quality_id



async def main():
    request_executor = CommonRequestExecutor()
    url = URL.create(
        'postgresql+asyncpg',
        username=os.getenv('db_user'),
        password=os.getenv('db_password'),
        port=os.getenv('db_port'),
        host=os.getenv('db_host'),
        database=os.getenv('db_name')
    )
    database = SkinDatabase(url)
    await database.drop_all_tables(Base.metadata)
    await database.proceed_schemas(Base.metadata)
    filler = DBFiller(database, SkinDatabaseService(request_executor), CsWikiService(request_executor))
    await filler.fill()


asyncio.run(main())



