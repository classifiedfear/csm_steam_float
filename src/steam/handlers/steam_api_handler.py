from typing import Tuple, List

from src.misc.dto import SkinDTO, SteamParamsDTO
from src.steam.links.steam_link import SteamLinkCreator
from src.steam.parsers.steam_api_parser import ParsedSteamMarketSkinDTO


class ParamHandler:
    @staticmethod
    def get_params(parsed_skin_dto: ParsedSteamMarketSkinDTO) -> SteamParamsDTO:
        first_two_param_text, last_two_param_text = ParamHandler._get_params_attr(
            parsed_skin_dto.inspect_skin_link
        )
        param_s, param_m = ParamHandler._get_param_s_and_m(first_two_param_text, parsed_skin_dto.listing_id)
        param_d, param_a = ParamHandler._get_param_d_and_a(last_two_param_text, parsed_skin_dto.asset_id)
        return SteamParamsDTO(param_s, param_m, param_a, param_d)

    @staticmethod
    def _get_params_attr(inspect_skin_link: str) -> List[str]:
        put_away_unnecessary = inspect_skin_link.replace(
            'steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20', ''
        )
        split_by_half = put_away_unnecessary.split('A')
        return split_by_half

    @staticmethod
    def _get_param_s_and_m(text: str, listing_id: int) -> Tuple[int, int]:
        return (listing_id, 0) if text.startswith('S') else (0, listing_id)

    @staticmethod
    def _get_param_d_and_a(text: str, asset_id: int) -> Tuple[int, int]:
        d_attr = text.split('D')
        param_d = int(d_attr[1])
        return param_d, asset_id


class SteamSkinHandler:
    @staticmethod
    def get_buy_link(unhandled_skin: ParsedSteamMarketSkinDTO, skin_dto: SkinDTO) -> str:
        base_root = SteamLinkCreator().create(skin_dto)
        return (base_root + f'?filter=#buylisting|'
                            f'{unhandled_skin.listing_id}|'
                            f'{unhandled_skin.app_id}|'
                            f'{unhandled_skin.context_id}|'
                            f'{unhandled_skin.asset_id}'
                )

    @staticmethod
    def get_price(unhandled_skin: ParsedSteamMarketSkinDTO) -> float:
        price = str(unhandled_skin.converted_price_per_unit + unhandled_skin.converted_fee_per_unit)
        price = price[0:-2] + '.' + price[-2:]
        return float(price)

    @staticmethod
    def get_inspect_link(parsed_skin_dto: ParsedSteamMarketSkinDTO) -> str:
        return (
            parsed_skin_dto.inspect_skin_link
            .replace("%listingid%", str(parsed_skin_dto.listing_id))
            .replace('%assetid%', str(parsed_skin_dto.asset_id))
        )

