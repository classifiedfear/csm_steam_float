from typing import List

from src.misc.exceptions import RequestError


class CsmAssetIdParser:
    @staticmethod
    def parse(response: dict):
        CsmAssetIdParser._check_response(response)
        return CsmAssetIdParser._find_asset_id_list(response)

    @staticmethod
    def _find_asset_id_list(response: dict) -> List[int]:
        asset_id_list = []
        for item in response['items']:
            if (overpay := item.get('overpay')) and (overpay.get('float')):
                asset_id_list.append(item['assetId'])
        return asset_id_list

    @staticmethod
    def _check_response(response: dict):
        if response.get('error'):
            raise RequestError('No more data available, or invalid skin info')