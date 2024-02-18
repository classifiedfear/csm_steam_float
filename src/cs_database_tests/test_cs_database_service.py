import pytest

from src.csgo_database.services.csgo_database_service import SkinDatabaseService
from src.misc.response_getter import CommonRequestExecutor


@pytest.mark.asyncio
async def test_cs_database_service():
    common_request_executor = CommonRequestExecutor()
    cs_database_service = SkinDatabaseService(common_request_executor)
    result = await cs_database_service.get_skin_for_weapon('Nova')
    print(result)