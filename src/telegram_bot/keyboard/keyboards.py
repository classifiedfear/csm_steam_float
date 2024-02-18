import asyncio

from aiogram.types import ReplyKeyboardMarkup

from src.telegram_bot.db import TGSkinQueries
from src.telegram_bot.resources.constants import buttons_const
from src.telegram_bot.keyboard.keyboard_utils import KeyboardCreator


class Keyboards:
    def __init__(self):
        self._keyboards = {}

    def add_keyboard(self, name: str, keyboard: ReplyKeyboardMarkup) -> None:
        self._keyboards[name] = keyboard

    def remove_keyboard(self, name: str) -> None:
        del self._keyboards[name]

    def get_keyboard(self, name: str) -> ReplyKeyboardMarkup:
        return self._keyboards[name]



