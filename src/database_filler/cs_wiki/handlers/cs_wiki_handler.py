from typing import Tuple, List


class CsWikiHandler:
    @staticmethod
    def get_name(parsed) -> Tuple[str, str]:
        skin_name = parsed.get('name')
        skin_name = skin_name.partition('—')[0].partition('|')
        return skin_name[0].strip(), skin_name[2].strip()

    @staticmethod
    def get_qualities(parsed) -> List[str]:
        return list(set(parsed.get('qualities')))

    @staticmethod
    def get_stattrak_existence(parsed) -> int:
        return parsed.get('stattraks')

