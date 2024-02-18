import pytest
import pytest_unordered


from src.database_filler.cs_wiki.services.cs_wiki_service import CsWikiService
from src.misc.dto import SkinDTO, DBSkinFiller
from src.misc.response_getter import CommonRequestExecutor


@pytest.fixture
def desert_eagle_skin_dto() -> SkinDTO:
    return SkinDTO('desert eagle', 'code red', 'Field-Tested', False)


@pytest.fixture
def csm_wiki_service():
    request_executor = CommonRequestExecutor()
    service = CsWikiService(request_executor)
    return service


@pytest.mark.asyncio
async def test_should_get_dto_expanded_skin_data(desert_eagle_skin_dto, csm_wiki_service):
    service = csm_wiki_service

    result = await service.get_skin('desert eagle', 'code red')

    assert result == DBSkinFiller(
        'Desert Eagle', 'Code Red', pytest_unordered.unordered(['Field-Tested', 'Well-Worn', 'Minimal Wear', 'Battle-Scarred', 'Factory New']), 2)




