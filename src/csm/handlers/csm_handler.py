from decimal import localcontext, Decimal

from src.csm.parsers.csm_skin_parser import ParsedCsmDTO


class CsmInfoHandler:

    @staticmethod
    def get_price(unhandled_cs_wiki_info: ParsedCsmDTO) -> float:
        with localcontext() as context:
            price_with_csm_percent = unhandled_cs_wiki_info.price - (unhandled_cs_wiki_info.price / 100 * 8)
            context.prec = 4
            return float(Decimal(price_with_csm_percent) * 1)

    @staticmethod
    def get_overpay_float_price(unhandled_cs_wiki_info: ParsedCsmDTO) -> float:
        default_price = CsmInfoHandler.get_price(unhandled_cs_wiki_info)
        with localcontext() as context:
            context.prec = 4
            return float(Decimal(default_price + unhandled_cs_wiki_info.overpay_float) * 1)

