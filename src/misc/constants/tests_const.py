from src.misc.constants.link_const import CSM_LINK_BASE_ROOT, STEAM_MARKET_LINK_BASE_ROOT

RESULT_CSM_WIKI_AK_47_LINK = 'https://wiki.cs.money/weapons/ak-47/asiimov'
RESULT_CSM_WIKI_DESERT_EAGLE_LINK = 'https://wiki.cs.money/weapons/desert-eagle/code-red'


RESULT_CSM_AK_47_LINK = (
    f'{CSM_LINK_BASE_ROOT}'
    f'?hasTradeLock=false&isStatTrak=false&limit=60&name=AK-47%20Asiimov&offset=0&quality=ft')

RESULT_CSM_DESERT_EAGLE_LINK = (
    f'{CSM_LINK_BASE_ROOT}'
    f'?hasTradeLock=false&isStatTrak=true&limit=60&name=Desert%20Eagle%20Code%20Red&offset=0&quality=bs'
)

RESULT_CSM_SPECIFIC_SKIN_LINK = (
    'https://cs.money/skin_info?appId=730&id=34622092793&isBot=true&botInventory=true'
)

RESULT_STEAM_DESERT_EAGLE_LINK = (
    f'{STEAM_MARKET_LINK_BASE_ROOT}'
    'Desert%20Eagle%20%7C%20Code%20Red%20%28Field-Tested%29'
)
RESULT_STEAM_AK_47_LINK = (
    f'{STEAM_MARKET_LINK_BASE_ROOT}'
    'StatTrak™%20AK-47%20%7C%20Asiimov%20%28Field-Tested%29'
)

RESULT_STEAM_API_AK_47_LINK = (
    f'{STEAM_MARKET_LINK_BASE_ROOT}'
    'StatTrak™%20AK-47%20%7C%20Asiimov%20%28Field-Tested%29/render/?start=0&count=100&currency=1'
)

RESULT_STEAM_API_DESERT_EAGLE_LINK = (
    f'{STEAM_MARKET_LINK_BASE_ROOT}'
    'Desert%20Eagle%20%7C%20Code%20Red%20%28Field-Tested%29/render/?start=0&count=100&currency=1'
)