import abc
from typing import Self


class TgMsgHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self):
        pass

    @staticmethod
    def is_composite() -> bool:
        return False


class TgMsgCompositeHandler(TgMsgHandler):

    def __init__(self):
        self._handlers = set()

    @staticmethod
    def is_composite() -> bool:
        return True

    def add(self, handler: TgMsgHandler) -> Self:
        self._handlers.add(handler)
        return self

    def remove(self, handler: TgMsgHandler) -> Self:
        self._handlers.remove(handler)
        return self

    async def handle(self):
        for handler in self._handlers:
            await handler.handle()

