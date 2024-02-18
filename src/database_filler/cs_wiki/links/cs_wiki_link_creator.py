from src.misc.constants import link_const
from src.misc.dto import SkinDTO
from src.misc.link_tools import LinkBuilder


class CsWikiLink:
    @staticmethod
    def create(weapon: str, skin: str) -> str:
        return (LinkBuilder(link_const.CSM_WIKI_LINK_BASE_ROOT)
                .add_part_link(CsWikiLink._weapon_link_part(weapon) + '/')
                .add_part_link(CsWikiLink._skin_link_part(skin) + '/')
                .build())

    @staticmethod
    def _weapon_link_part(weapon: str) -> str:
        return weapon.lower().replace(' ', '-')

    @staticmethod
    def _skin_link_part(skin: str) -> str:
        return skin.lower().replace("'", '').replace(' ', '-')
