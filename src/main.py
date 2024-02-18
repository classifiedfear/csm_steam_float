import asyncio
import logging
import os
import sys

from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler import AsyncScheduler
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore

from redis import asyncio as aioredis

from src.telegram_bot.db import TGSkinQueries
from src.telegram_bot.db.skindatabase import SkinDatabase

from src.telegram_bot import handlers
from src.telegram_bot.keyboard.keyboard_utils import KeyboardCreator
from src.telegram_bot.keyboard.keyboards import Keyboards
from src.telegram_bot.resources.constants import buttons_const


class Application:
    def __init__(self) -> None:
        self.redis = aioredis.Redis()
        self.dp = Dispatcher(storage=RedisStorage(self.redis))
        self.bot = Bot(token=os.getenv('token'), parse_mode=ParseMode.HTML)




    async def __init_handlers(self, scheduler: AsyncScheduler) -> handlers.TgMsgCompositeHandler:
        #self._settings_router = Router()
        self._command_router = Router()
        #self._other_router = Router()
        self._KEYBOARDS = Keyboards()
        self._KEYBOARDS.add_keyboard(
            'main_menu',
            KeyboardCreator.create_reply_keyboard(buttons_const.MAIN_MENU_KEYBOARD_TEXT_LIST, 2, 2, 1)
        )
        self._KEYBOARDS.add_keyboard(
            'skin_menu',
            KeyboardCreator.create_reply_keyboard(await TGSkinQueries.get_skins_for_weapon('AK-47'))
        )
        general_handler = handlers.TgMsgCompositeHandler()
        command_handler = handlers.TgCommandMsgHandler(self._command_router, self._KEYBOARDS)
        #setting_handler = handlers.SettingHandler(self._settings_router, RedisController(redis=self.redis))
        #other_handler = handlers.OtherHandler(self._other_router)
        general_handler.add(command_handler)
        return general_handler

    async def main(self) -> None:
        data_store = SQLAlchemyDataStore(engine=SkinDatabase.ENGINE)
        async with AsyncScheduler(data_store=data_store) as scheduler:
            general_handler = await self.__init_handlers(scheduler)
            await general_handler.handle()
            self.dp.include_routers(self._command_router)
            await scheduler.start_in_background()
            await self.dp.start_polling(self.bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app = Application()
    try:
        asyncio.run(app.main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped!')
