from src.database_filler.cs_wiki.handlers.cs_wiki_handler import CsWikiHandler
from src.database_filler.cs_wiki.links.cs_wiki_link_creator import CsWikiLink
from src.database_filler.cs_wiki.parsers.cs_wiki_parser import CsWikiParser
from src.misc.dto import DBSkinFiller
from src.misc.response_getter import CommonRequestExecutor


class CsWikiService:
    def __init__(self, request_executor: CommonRequestExecutor) -> None:
        self._request_executor = request_executor

    async def get_skin(self, weapon: str, skin: str) -> DBSkinFiller:
        response = await self._request_executor.get_response_text(CsWikiLink.create(weapon, skin))
        parsed_skin = CsWikiParser.parse(response)
        return self._handle_skin(parsed_skin)

    @staticmethod
    def _handle_skin(parsed) -> DBSkinFiller:
        weapon, skin = CsWikiHandler.get_name(parsed)
        qualities = CsWikiHandler.get_qualities(parsed)
        stattrak_existence = CsWikiHandler.get_stattrak_existence(parsed)
        return DBSkinFiller(
            weapon, skin, qualities, stattrak_existence
        )

