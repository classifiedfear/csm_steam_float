from src.misc.dto import SkinDTO

from src.misc.constants import link_const
from src.misc.link_tools import LinkBuilder


class CsmLinkCreator:

    @staticmethod
    def create(skin_data: SkinDTO, *, limit: int = 60, offset: int = 0) -> str:
        return (LinkBuilder(link_const.CSM_LINK_BASE_ROOT).add_param('hasTradeLock', 'false')
                .add_param('isStatTrak', CsmLinkCreator._get_stattrak_link_part(skin_data))
                .add_param('limit', str(limit))
                .add_param('name', f"{CsmLinkCreator._get_weapon_link_part(skin_data)}")
                .add_part_link(f'%20{CsmLinkCreator._get_skin_link_part(skin_data)}')
                .add_param('offset', str(offset))
                .add_param('quality', CsmLinkCreator._get_quality_link_part(skin_data))
                .build()
                )

    @staticmethod
    def _get_skin_link_part(skin_data: SkinDTO):
        return '%20'.join(skin_data.skin.split())

    @staticmethod
    def _get_quality_link_part(skin_data: SkinDTO):
        csm_quality = skin_data.quality[0]
        for index, letter in enumerate(skin_data.quality):
            if letter == ' ' or letter == '-':
                csm_quality += skin_data.quality[index + 1]
        return csm_quality.lower()

    @staticmethod
    def _get_weapon_link_part(skin_data: SkinDTO):
        return '%20'.join(skin_data.weapon.split())

    @staticmethod
    def _get_stattrak_link_part(skin_data: SkinDTO):
        return 'true' if skin_data.stattrak else 'false'



print(CsmLinkCreator().create(SkinDTO('Desert Eagle', 'Code Red', 'Field-Tested', False)))


