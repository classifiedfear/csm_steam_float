import pytest

from src.misc.constants import tests_const
from src.misc.dto import SkinDTO
from src.steam.links.steam_api_link import ApiSteamLinkCreator
from src.steam.links.steam_link import SteamLinkCreator


@pytest.mark.parametrize(
    ('skin_dto', 'expected'),
    (
        (SkinDTO('AK-47', 'Asiimov', 'Field-Tested', True), tests_const.RESULT_STEAM_AK_47_LINK),
        (SkinDTO('Desert Eagle', 'Code Red', 'Field-Tested', False), tests_const.RESULT_STEAM_DESERT_EAGLE_LINK)
    )
)
def test_should_create_link_for_steam(skin_dto, expected):
    result = SteamLinkCreator.create(skin_dto)
    assert result == expected


@pytest.mark.parametrize(
    ('skin_dto', 'expected'),
    (
        (SkinDTO('AK-47', 'Asiimov', 'Field-Tested', True), tests_const.RESULT_STEAM_API_AK_47_LINK),
        (SkinDTO('Desert Eagle', 'Code Red', 'Field-Tested', False), tests_const.RESULT_STEAM_API_DESERT_EAGLE_LINK)
    )
)
def test_should_create_link_for_steam_api(skin_dto, expected):
    result = ApiSteamLinkCreator.create(skin_dto, count=100)
    assert result == expected

