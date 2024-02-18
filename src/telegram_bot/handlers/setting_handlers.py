from __future__ import annotations

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from redis_controller import RedisController
from src.telegram_bot.handlers import TgMsgHandler
from src.telegram_bot.midlewares.settings_check import SettingsCheck
from src.telegram_bot.states import SettingStates
from src.telegram_bot.resources import constants


class SettingHandler(TgMsgHandler):
    def __init__(self, router: Router, redis_controller: RedisController):
        self._router = router
        self._controller = redis_controller
        self._router.message.middleware(SettingsCheck(self._controller))

    async def handle(self) -> None:
        @self._router.message(F.text == constants.buttons_const.SETTINGS_TEXT)
        async def general_settings(
                message: Message, state: FSMContext, stattrak_setting: bool, quality_setting: str, search_setting: bool
        ) -> None:
            await state.set_state(SettingStates.GENERAL_SETTINGS)
            await message.answer(
                constants.from_bot.settings_msg_const.SETTINGS_MSG.format(
                    quality_setting,
                    constants.from_bot.common_msg.ON if stattrak_setting else constants.from_bot.common_msg.OFF,
                    constants.from_bot.common_msg.ON if search_setting else constants.from_bot.common_msg.OFF
                ),
                reply_markup=KEYBOARDS.get_keyboard('settings_menu')
            )

        @self._router.message(
            SettingStates.GENERAL_SETTINGS,
            F.text == constants.from_bot.settings_msg_const.CHANGE_QUALITY_MSG_SETTING
        )
        async def quality_settings(message: Message, state: FSMContext) -> None:
            await state.set_state(SettingStates.QUALITY_SETTINGS)
            await message.answer(
                constants.from_bot.settings_msg_const.CHOOSE_QUALITY_MSG_SETTING,
                reply_markup=KEYBOARDS.get_keyboard('quality_settings')
            )

        @self._router.message(
            SettingStates.QUALITY_SETTINGS,
            lambda message: message.text in constants.skin_const.Qualities.get_qualities()
        )
        async def set_quality(message: Message, state: FSMContext) -> None:
            await self._controller.set_quality(message.from_user.id, message.text)
            await message.answer(
                constants.from_bot.common_msg.SAVE_SETTINGS.format(
                    setting=constants.from_bot.common_msg.QUALITY_SETTING, state=message.text
                ),
                reply_markup=KEYBOARDS.get_keyboard('main_menu')
            )
            await state.clear()

        @self._router.message(
            SettingStates.GENERAL_SETTINGS,
            F.text == constants.from_bot.settings_msg_const.CHANGE_STATTRAK_MSG_SETTING
        )
        async def stattrak_settings(message: Message, state: FSMContext) -> None:
            await state.set_state(SettingStates.STATTRAK_SETTINGS)
            await message.answer(
                constants.from_bot.settings_msg_const.CHOOSE_STATTRAK_MSG_SETTING,
                reply_markup=KEYBOARDS.get_keyboard('bool_settings')
            )

        @self._router.message(
            SettingStates.STATTRAK_SETTINGS,
            lambda message: message.text in {
                constants.from_bot.settings_msg_const.STATE_ON_MSG_SETTING,
                constants.from_bot.settings_msg_const.STATE_OFF_MSG_SETTING}
        )
        async def set_stattrak(message: Message, state: FSMContext) -> None:
            stattrak_setting = _setting_state(message.text)
            await self._controller.set_stattrak(message.from_user.id, stattrak_setting)
            await message.answer(
                constants.from_bot.common_msg.SAVE_SETTINGS.format(
                    setting=constants.from_bot.common_msg.STATTRAK_SETTING,
                    state=constants.from_bot.common_msg.ON if stattrak_setting else constants.from_bot.common_msg.OFF
                ),
                reply_markup=KEYBOARDS.get_keyboard('main_menu')
            )

            await state.clear()

        @self._router.message(
            SettingStates.GENERAL_SETTINGS,
            F.text == constants.from_bot.settings_msg_const.CHANGE_SEARCH_MSG_SETTING
        )
        async def search_settings(message: Message, state: FSMContext) -> None:
            await state.set_state(SettingStates.SEARCH_STATE)
            await message.answer(
                constants.from_bot.settings_msg_const.CHOOSE_SEARCH_MSG_SETTING,
                reply_markup=KEYBOARDS.get_keyboard('bool_settings')
            )

        @self._router.message(
            SettingStates.SEARCH_STATE,
            lambda message: message.text in {
                constants.from_bot.settings_msg_const.STATE_ON_MSG_SETTING,
                constants.from_bot.settings_msg_const.STATE_OFF_MSG_SETTING}
        )
        async def set_search(message: Message, state: FSMContext) -> None:
            search_setting = _setting_state(message.text)
            await self._controller.set_search(message.from_user.id, search_setting)
            await message.answer(
                constants.from_bot.common_msg.SAVE_SETTINGS.format(
                    setting=constants.from_bot.common_msg.SEARCH_SETTING,
                    state=constants.from_bot.common_msg.ON if search_setting else constants.from_bot.common_msg.OFF),
                reply_markup=KEYBOARDS.get_keyboard('main_menu')
            )

            await state.clear()

        def _setting_state(text: str) -> bool:
            if text == constants.from_bot.settings_msg_const.STATE_ON_MSG_SETTING:
                return True
            elif text == constants.from_bot.settings_msg_const.STATE_OFF_MSG_SETTING:
                return False

        






