from __future__ import annotations

from typing import List

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, KeyboardBuilder


class KeyboardCreator:
    @staticmethod
    def create_reply_keyboard(buttons_text: List[str], *sizes, **kwargs) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        return KeyboardCreator._create_keyboard(builder, buttons_text, *sizes, **kwargs)

    @staticmethod
    def create_inline_keyboard(
            buttons_text: List[str], *sizes, **kwargs) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        return KeyboardCreator._create_keyboard(builder, buttons_text, *sizes, **kwargs)

    @staticmethod
    def _create_keyboard(builder: KeyboardBuilder, buttons_text: List[str], *sizes, **kwargs):
        for text in buttons_text:
            builder.button(text=text, **kwargs)
            builder.adjust(*sizes)
        return builder.as_markup()

