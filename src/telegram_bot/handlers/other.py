from __future__ import annotations


from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.telegram_bot.handlers import TgMsgHandler

from src.telegram_bot.states import SettingStates
from src.telegram_bot.resources import constants


class OtherHandler(TgMsgHandler):
    def __init__(self, router: Router):
        self._router = router

    async def handle(self) -> None:
        @self._router.message(F.text == constants.from_bot.common_msg.BACK_TO_MAIN_MENU)
        async def back_to_main_manu(message: Message, state: FSMContext) -> None:
            await message.answer(
                constants.from_bot.common_msg.ACTION_BACK_TO_MAIN_MENU,
                reply_markup=KEYBOARDS.get_keyboard('main_menu')
            )
            await state.clear()
            return

        @self._router.message(F.text == constants.from_bot.common_msg.BACK)
        async def back(message: Message, state: FSMContext) -> None:
            await message.answer(
                constants.from_bot.common_msg.ACTION_BACK,
                reply_markup=KEYBOARDS.get_keyboard('settings_menu')
            )
            await state.set_state(SettingStates.GENERAL_SETTINGS)


