import random

from src.misc.constants import link_const
from src.misc.dto import SkinDTO
from src.misc.link_tools import LinkBuilder
from src.steam.links.steam_link import SteamLinkCreator


class ApiSteamLinkCreator(SteamLinkCreator):
    @staticmethod
    def create(skin_dto: SkinDTO, *, start: int = 0, count: int = 10, currency: int = 1) -> str:
        return (
            LinkBuilder(link_const.STEAM_MARKET_LINK_BASE_ROOT)
            .add_part_link(ApiSteamLinkCreator._stattrak_link_part(skin_dto))
            .add_part_link(ApiSteamLinkCreator._weapon_link_part(skin_dto))
            .add_part_link(ApiSteamLinkCreator._skin_link_part(skin_dto))
            .add_part_link(ApiSteamLinkCreator._quality_link_part(skin_dto))
            .add_part_link('/render/')
            .add_param('query', '')
            .add_param('start', str(start))
            .add_param('count', str(count))
            .add_param('country', random.choice(['UA', 'PL', 'US', 'CA', 'CZ', 'FR', 'DE']))
            .add_param('language', 'english')
            .add_param('currency', str(currency))
            .build()
        )

