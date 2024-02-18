from src.misc.constants import link_const
from src.misc.link_tools import LinkBuilder


class CsmSkinLinkCreator:

    @staticmethod
    def create(asset_id: int = 34622092793):
        return (LinkBuilder(link_const.CSM_LINK_SKIN_INFO_BASE_ROOT)
                .add_param('appId', '730')
                .add_param('id', str(asset_id))
                .add_param('isBot', 'true')
                .add_param('botInventory', 'true')
                .build()
                )