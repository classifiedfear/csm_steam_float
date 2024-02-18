from src.misc.dto import ParsedCsmDTO


class CsmSkinParser:
    @staticmethod
    def parse(response: dict) -> ParsedCsmDTO:
        skin_name = response['fullName']
        skin_price = response['defaultPrice']
        overpay_float = response['overpay']['float']
        skin_float = response['float']
        return ParsedCsmDTO(skin_name, skin_price, overpay_float, float(skin_float))

