import asyncio
from collections import defaultdict
from decimal import localcontext, Decimal
from typing import List, Tuple

from src.misc.dto import SkinDTO, CsmSkinDTO, CsmSteamMatchedSkin, SteamSkinDTO
from src.misc.exceptions import RequestError
from src.misc.response_getter import CommonRequestExecutor
from src.steam.services.steam_api_service import ApiSteamCsMarketService
from src.csm.services.csm_service import CsmService
from src.misc.link_tools import Pager


class CsmSteamService:
    def __init__(self, csm_service: CsmService, steam_service: ApiSteamCsMarketService):
        self._csm_service = csm_service
        self._steam_service = steam_service

    async def csm_parse(self, skin_dto: SkinDTO):
        skins = []
        pager: Pager = Pager(60)
        while True:
            try:
                skins.extend(await self._csm_service.get_market_skins(
                    skin_dto, limit=pager.page_size, offset=pager.get_next_offset()
                ))
            except RequestError:
                break
        return skins

    async def steam_parse(self, skin_dto: SkinDTO):
        #pager: Pager = Pager(10)
        #for page in range(2):
        skins = []
        skins.extend(await self._steam_service.get_market_skins(skin_dto))
        return skins


class CsmSteamMatchingSkinFinder:
    def __init__(self, steam_csm_service: CsmSteamService):
        self._steam_csm_service = steam_csm_service

    async def match(self, skin_dto: SkinDTO) -> List[CsmSteamMatchedSkin] | None:
        csm_skins, steam_skins = await asyncio.gather(
            self._steam_csm_service.csm_parse(skin_dto), self._steam_csm_service.steam_parse(skin_dto)
        )
        if not (csm_skins or steam_skins):
            return
        return await self._get_matching_skins(csm_skins, steam_skins)

    async def _get_matching_skins(self, csm_skins: List[CsmSkinDTO], steam_skins: List[SteamSkinDTO]):
        with localcontext() as context:
            context.prec = 2
            steam_skins = self._create_dict_by_floats(steam_skins)
            return await self._compare(csm_skins, steam_skins)

    async def _compare(
            self, csm_skins: List[CsmSkinDTO], steam_skins: defaultdict[Decimal, List[SteamSkinDTO]]
    ):
        tasks = []
        for index in range(len(csm_skins)):
            tasks.append(self._get_max_matched_skin_if_exists(csm_skins[index], steam_skins))
        result = await asyncio.gather(*tasks)
        return self._get_list_without_none_values(result)

    async def _get_max_matched_skin_if_exists(self, csm_skin, steam_skins):
        if matched_by_float_steam_skins := self._get_matched_steam_skins_by_float_if_exists(csm_skin, steam_skins):
            if matched_by_percent := self._get_csm_steam_matched_by_percent(csm_skin, matched_by_float_steam_skins):
                return max(matched_by_percent, key=lambda matched_skin: matched_skin.price_percent)
        return None

    @staticmethod
    def _get_list_without_none_values(skins: Tuple[CsmSteamMatchedSkin]):
        return [skin for skin in skins if skin]

    @staticmethod
    def _get_matched_steam_skins_by_float_if_exists(csm_skin, steam_skins):
        csm_float = Decimal(csm_skin.skin_float) * 1
        return steam_skins.get(csm_float)

    def _get_csm_steam_matched_by_percent(self, csm_skin, matched_by_float_steam_skins) -> List[CsmSteamMatchedSkin]:
        return [
                CsmSteamMatchedSkin(steam_skin, csm_skin, percent) for steam_skin in matched_by_float_steam_skins if
                (percent := self._find_percent(csm_skin, steam_skin)) >= 10
        ]

    @staticmethod
    def _create_dict_by_floats(steam_skins: List[SteamSkinDTO]) -> defaultdict[Decimal, List[SteamSkinDTO]]:
        floats_steam_dto = defaultdict(list)
        for steam_skin_dto in steam_skins:
            steam_float = Decimal(steam_skin_dto.skin_float) * 1
            floats_steam_dto[steam_float].append(steam_skin_dto)
        return floats_steam_dto

    @staticmethod
    def _find_percent(csm_skin: CsmSkinDTO, steam_skin: SteamSkinDTO):
        return int(100 - ((steam_skin.price * 100) // csm_skin.price_with_float))



common_request_executor = CommonRequestExecutor()
steam_service = CsmSteamService(CsmService(common_request_executor), ApiSteamCsMarketService(common_request_executor))
print(asyncio.run(CsmSteamMatchingSkinFinder(steam_service).match(SkinDTO('AK-47', 'Asiimov', 'Battle-Scarred', False))))