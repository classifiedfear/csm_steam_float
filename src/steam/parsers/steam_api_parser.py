import asyncio

import logging

from typing import Tuple, List

from src.misc.dto import ParsedSteamMarketSkinDTO, SkinDTO
from src.misc.exceptions import RequestError
from src.misc.response_getter import CommonRequestExecutor
from src.steam.links.steam_api_link import ApiSteamLinkCreator

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)


class ApiSteamCsMarketParser:
    @staticmethod
    def parse(response: dict) -> List[ParsedSteamMarketSkinDTO]:
        ApiSteamCsMarketParser._check_response(response)
        return ApiSteamCsMarketParser._find_skins_data(response['listinginfo'])

    @staticmethod
    def _check_response(response: dict):
        if (response is None) or (not response['listinginfo']):
            raise RequestError('To many request')

    @staticmethod
    def _find_skins_data(listing: dict) -> List[ParsedSteamMarketSkinDTO]:
        skins = []
        for item in listing.values():
            skins.append(ApiSteamCsMarketParser._find_skin(item))
        return skins

    @staticmethod
    def _find_skin(item: dict) -> ParsedSteamMarketSkinDTO:
        asset = item['asset']
        return ParsedSteamMarketSkinDTO(
            int(asset['id']),
            int(item['listingid']),
            int(asset['appid']),
            int(asset['contextid']),
            asset['market_actions'][0]['link'],
            item['converted_price_per_unit'],
            item['converted_fee_per_unit'],
        )
