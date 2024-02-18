from src.float_checker.links.float_checker_link_creator import FloatCheckerLinkCreator
from src.misc.response_getter import CommonRequestExecutor


class FloatCheckerService:
    def __init__(self, request_executor: CommonRequestExecutor):
        self._request_executor = request_executor
        self._headers = {'Origin': 'https://csfloat.com'}

    async def get_item_info(self, inspect_link: str):
        link = FloatCheckerLinkCreator.create(inspect_link)
        response = await self._request_executor.get_response_json(link, headers=self._headers)
        return response

