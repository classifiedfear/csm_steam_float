from typing import List

import pytest


from src.csm.services.csm_service import CsmService
from src.misc.dto import CsmSkinDTO, SkinDTO
from src.misc.exceptions import RequestError
from src.misc.link_tools import Pager
from src.misc.response_getter import CommonRequestExecutor


@pytest.fixture
def ak_47_skin_dto():
    return SkinDTO(
        'AK-47', 'Asiimov', 'Battle-Scarred', False
    )


@pytest.fixture
def service() -> CsmService:
    request_executor = CommonRequestExecutor()
    service = CsmService(request_executor)
    return service


@pytest.mark.asyncio
async def test_should_get_csm_list_skin_data_dto(ak_47_skin_dto, service):
    result = await service.get_market_skins(ak_47_skin_dto)
    _should_equal_tuple_with_csm_skin_dtos(result)


@pytest.mark.asyncio
async def test_should_get_csm_skin_dto_list_from_all_pages(ak_47_skin_dto, service):
    pager = Pager(60)
    while True:
        try:
            response = await service.get_market_skins(
                ak_47_skin_dto, limit=pager.page_size, offset=pager.get_next_offset()
            )
            _should_equal_tuple_with_csm_skin_dtos(response)
        except RequestError:
            break


def _should_equal_tuple_with_csm_skin_dtos(result: List[CsmSkinDTO]):
    assert result
    for skin_dto in result:
        assert skin_dto.name == 'AK-47 | Asiimov (Battle-Scarred)'
        assert isinstance(skin_dto.skin_float, float)
        assert isinstance(skin_dto.price, float)
        assert isinstance(skin_dto.overpay_float, float)

