import dataclasses
from typing import List


@dataclasses.dataclass
class SkinDTO:
    weapon: str
    skin: str
    quality: str
    stattrak: bool


@dataclasses.dataclass
class DBSkinFiller:
    weapon: str
    skin: str
    qualities: List[str]
    stattrak_existence: int


@dataclasses.dataclass
class CsmSkinDTO:
    name: str
    skin_float: float
    price: float
    price_with_float: float
    overpay_float: float


@dataclasses.dataclass
class SteamSkinDTO:
    name: str
    price: float
    link: str
    skin_float: float


@dataclasses.dataclass
class ParsedSteamMarketSkinDTO:
    asset_id: int
    listing_id: int
    app_id: int
    context_id: int
    inspect_skin_link: str
    converted_price_per_unit: str
    converted_fee_per_unit: str


@dataclasses.dataclass
class SteamParamsDTO:
    param_s: int
    param_m: int
    param_a: int
    param_d: int


@dataclasses.dataclass
class ParsedCsmDTO:
    name: str
    price: float
    overpay_float: float
    skin_float: float



@dataclasses.dataclass
class CsmSteamMatchedSkin:
    steam_skin_dto: SteamSkinDTO
    csm_skin_dto: CsmSkinDTO
    price_percent: int

