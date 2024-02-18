import pytest

from src.misc.dto import SkinDTO
from src.misc.response_getter import CommonRequestExecutor
from src.steam.links.steam_api_link import ApiSteamLinkCreator


@pytest.fixture
def common_request_executor():
    return CommonRequestExecutor()

@pytest.mark.asyncio
async def test_should_get_json_response_steam_page(common_request_executor):
    link = ApiSteamLinkCreator.create(SkinDTO('USP-S', 'Cortex', 'Field-Tested', False))
    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Host': 'steamcommunity.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Prototype-Version': '1.7',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = await common_request_executor.get_response_json(link, headers=headers)
    print(response)
    assert response is not None and response['listinginfo']