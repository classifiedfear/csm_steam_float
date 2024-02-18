import pytest

from src.misc.response_getter import CommonRequestExecutor
from src.float_checker.float_checker_service import FloatCheckerService

@pytest.mark.asyncio
async def test_should_get_float():
    float_service = FloatCheckerService(CommonRequestExecutor())
    print(await float_service.get_item_info('steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M4720404381237057706A35722649388D14333845246457160659'))

