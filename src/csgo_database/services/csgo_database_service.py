

from src.csgo_database.links.cs_database_weapon_link_creator import CsgoDatabaseSkinsLinkCreator, CsgoDatabaseWeaponsLinkCreator
from src.csgo_database.parsers.skin_database_parser import SkinCsgoDatabaseParser, CsgoDatabaseParser
from src.misc.response_getter import CommonRequestExecutor
from src.telegram_bot.resources.constants import skin_const


class SkinDatabaseService:
    def __init__(self, common_request_executor: CommonRequestExecutor):
        self._common_request_executor = common_request_executor

    async def get_skin_for_weapon(self, weapon: str):
        response = await self._common_request_executor.get_response_text(CsgoDatabaseSkinsLinkCreator.create(weapon))
        return SkinCsgoDatabaseParser.parse(response)

    async def get_weapons(self):
        response = await self._common_request_executor.get_response_text(CsgoDatabaseWeaponsLinkCreator.create())
        return CsgoDatabaseParser.parse(response)

