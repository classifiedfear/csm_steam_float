import aiogram
from aiogram import types
from aiogram import filters


from src.telegram_bot.handlers.handlers import TgMsgHandler
from src.telegram_bot.resources import constants


class TgCommandMsgHandler(TgMsgHandler):
    def __init__(self, router: aiogram.Router, keyboards) -> None:
        self._router = router
        self._KEYBOARDS = keyboards

    async def handle(self):
        @self._router.message(aiogram.F.text == constants.buttons_const.DESC_TEXT)
        async def command_help(message: types.Message) -> None:
            await message.answer('Описание')

        @self._router.message(filters.CommandStart())
        async def command_start(message: types.Message) -> None:
            await message.answer(
                text=f'Привет, {message.from_user.full_name}',
                reply_markup=self._KEYBOARDS.get_keyboard('main_menu')
            )
        @self._router.message(aiogram.F.text == 'Изменение скина')
        async def change_skin(message: types.Message) -> None:
            await message.answer(
                text='Выберите скин',
                reply_markup=self._KEYBOARDS.get_keyboard('skin_menu')
            )