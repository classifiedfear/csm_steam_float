import asyncio

from typing import List

from src.csm.handlers.csm_handler import CsmInfoHandler
from src.csm.links.csm_link_creator import CsmLinkCreator
from src.csm.links.csm_skin_link_creator import CsmSkinLinkCreator
from src.csm.parsers.csm_asset_id_parser import CsmAssetIdParser
from src.csm.parsers.csm_skin_parser import CsmSkinParser, ParsedCsmDTO
from src.misc.dto import CsmSkinDTO, SkinDTO
from src.misc.response_getter import CommonRequestExecutor


class CsmService:
    def __init__(self, request_executor: CommonRequestExecutor) -> None:
        self._request_executor = request_executor

    async def get_market_skins(self, skin_dto: SkinDTO, *, limit: int = 60, offset: int = 0) -> List[CsmSkinDTO]:
        """Parse 1 page from csm_tests"""
        asset_id_list = await self._get_asset_id_list(skin_dto, limit, offset)
        parsed_skins = await self._get_parsed_skin_list(asset_id_list)
        return self._handle_list_skins(parsed_skins)

    async def _get_asset_id_list(self, skin_dto: SkinDTO, limit: int, offset: int):
        link = CsmLinkCreator.create(skin_dto, limit=limit, offset=offset)
        response = await self._request_executor.get_response_json(link)
        return CsmAssetIdParser.parse(response)

    async def _get_parsed_skin_list(self, asset_id_list: List[int]):
        tasks = []
        for asset_id in asset_id_list:
            link = CsmSkinLinkCreator.create(asset_id)
            task = asyncio.create_task(self._request_executor.get_response_json(link))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return [CsmSkinParser.parse(response) for response in responses]

    def _handle_list_skins(self, parsed_skins: List[ParsedCsmDTO]) -> List[CsmSkinDTO]:
        skins = []
        for parsed_skin in parsed_skins:
            skins.append(self._handle_skin(parsed_skin))
        return skins

    @staticmethod
    def _handle_skin(parsed_skin: ParsedCsmDTO):
        price = CsmInfoHandler.get_price(parsed_skin)
        price_with_float = CsmInfoHandler.get_overpay_float_price(parsed_skin)
        return CsmSkinDTO(
            parsed_skin.name, parsed_skin.skin_float, price, price_with_float, parsed_skin.overpay_float
        )
