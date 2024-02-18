import asyncio
from typing import List


from src.misc.dto import SkinDTO, SteamSkinDTO
from src.misc.response_getter import CommonRequestExecutor
from src.steam.handlers.steam_api_handler import SteamSkinHandler
from src.steam.links.steam_api_link import ApiSteamLinkCreator
from src.steam.parsers.steam_api_parser import ApiSteamCsMarketParser, ParsedSteamMarketSkinDTO
from src.float_checker.float_checker_service import FloatCheckerService


class ApiSteamCsMarketService:
    def __init__(self, request_executor: CommonRequestExecutor):
        self._request_executor = request_executor
        self._headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,ru;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'steamcommunity.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest'
            }

    async def get_market_skins(
            self, skin_dto: SkinDTO, *, start: int = 0, count: int = 10, currency: int = 1) -> List[SteamSkinDTO]:
        response = await self._request_executor.get_response_json(
            ApiSteamLinkCreator.create(skin_dto, start=start, count=count, currency=currency),
            headers=self._headers
        )
        parsed_skins = ApiSteamCsMarketParser.parse(response)
        return await self._handle_skins(parsed_skins, skin_dto)

    async def _handle_skins(self, parsed_skins_dto: List[ParsedSteamMarketSkinDTO], skin_dto: SkinDTO):
        tasks = []
        float_service = FloatCheckerService(self._request_executor)
        for parsed_skin_dto in parsed_skins_dto:
            task = asyncio.create_task(self._handle_skin(float_service, parsed_skin_dto, skin_dto))
            tasks.append(task)
        return [skin for skin in await asyncio.gather(*tasks)]

    @staticmethod
    async def _handle_skin(
            service: FloatCheckerService, parsed_skin_dto: ParsedSteamMarketSkinDTO, skin_dto: SkinDTO
    ):
        inspect_link = SteamSkinHandler.get_inspect_link(parsed_skin_dto)
        response = await service.get_item_info(inspect_link)
        item_info = response['iteminfo']
        skin_float = item_info['floatvalue']
        skin_name = item_info['full_item_name']
        buy_link = SteamSkinHandler.get_buy_link(parsed_skin_dto, skin_dto)
        skin_price = SteamSkinHandler.get_price(parsed_skin_dto)
        return SteamSkinDTO(skin_name, skin_price, buy_link, skin_float)


