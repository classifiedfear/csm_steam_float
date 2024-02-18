from src.misc.link_tools import LinkBuilder


class FloatCheckerLinkCreator:
    @staticmethod
    def create(inspect_link: str) -> str:
        return (
            LinkBuilder('https://api.csfloat.com/?url=').add_part_link(inspect_link).build()
        )