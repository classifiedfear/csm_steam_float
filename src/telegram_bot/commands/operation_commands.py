from abc import abstractmethod

from src.misc.dto import SkinDTO
from src.misc.exceptions import InvalidWeapon, InvalidSkin
from src.telegram_bot import settings
from src.telegram_bot.commands.abstact_command import BotCommand
from src.database_filler.cs_wiki.services.cs_wiki_service import CsWikiService


class BotParserCommands(BotCommand):
    def __init__(self, container: deque):
        self.container = container

    @abstractmethod
    async def execute(self):
        pass

    async def _parse_data(self, weapon: str, skin: str, quality: str, stattrak: bool):
        matching_data_provider = CsmSteamMatchingDataGetter(weapon, skin, quality, stattrak)
        async for item in matching_data_provider.compare_all_data():
            self.container.append(item)


class MsgParser:
    def __init__(self, cs_wiki_service: CsWikiService):
        self._cs_wiki_service = cs_wiki_service
        self._WEAPONS = (
            'p2000', 'usp-s', 'p250', 'mag-7', 'xm1014', 'mp9', 'mac-10',
            'mp7', 'mp5sd', 'ump-45', 'p90', 'famas', 'm4a1-s', 'm4a4',
            'aug', 'ak-47', 'scar-20', 'nova', 'g3sg1', 'awp', 'm249',
            'glock-18', 'negev', 'tec-9', 'five-seven', 'cz75-auto',
            'saved-off', 'pp-bizon', 'desert eagle', 'r8 revoulver', 'dual berettas',
            'sg 553', 'ssg 08', 'galil ar', 'karambit', 'm9 bayonet',
            'bayonet', 'butterfly', 'talon', 'skeleton', 'classic',
            'stiletto', 'ursus', 'paracord', 'nomad', 'survival', 'huntsman',
            'flip', 'bowie', 'falchion', 'gut', 'navaja', 'shadow daggers'
        )

    def execute(self, msg: str, stattrak_default: bool = False, quality_default: str = 'Field-Tested'):
        weapon, skin, quality, stattrak = self._construct_weapon_data_from_user_msg(msg)

        if weapon is None:
            raise InvalidWeapon

        if skin is None:
            raise InvalidSkin

        if quality is None:
            quality = quality_default

        if stattrak is None:
            stattrak = stattrak_default

        weapon_data = await self._get_correct_skin_data(weapon, skin, quality, stattrak)

        return weapon_data

    def _get_weapon_from(self, msg: str) -> str:




    async def _get_correct_skin_data(self, weapon: str, skin: str, quality: str, stattrak: bool):
        """Check if skin exists, if exists return correct name for data and qualities for that skin."""
        return await self._cs_wiki_service.get_skin(SkinDTO(weapon, skin, quality, stattrak))


    async def _construct_weapon_data_from_user_msg(self, msg: str):
        msg_split = [item.strip() for item in msg.lower().split(',')]
        weapon = None
        skin = None
        quality = None
        stattrak = None

        for index, item in enumerate(msg_split.copy()):
            if item in self._WEAPONS:
                weapon = item
                msg_split.remove(item)
            elif item in [data.lower() for data in settings.Quality.ENG.value]:
                quality = item
                self._user_weapon_msg.remove(item)
            elif item == 'stattrak':
                self._user_weapon_msg.remove(item)
                stattrak = True
            else:
                skin = item
                self._user_weapon_msg.remove(item)

        return weapon, skin, quality, stattrak


class UserMsgParserCommand(BotParserCommands):
    def __init__(
            self,
            weapon: str,
            skin: str,
            quality: str,
            stattrak: bool,
            container: deque,
    ) -> None:
        super().__init__(container=container)
        self.weapon = weapon
        self.skin = skin
        self.quality = quality
        self.stattrak = stattrak

    async def execute(self):
        await self._parse_data(self.weapon, self.skin, self.quality, self.stattrak)


class DBParserCommand(BotParserCommands):
    def __init__(self, container: deque):
        super().__init__(container=container)

    async def execute(self):
        if weapon_data := await db_query.get_random_weapon_from_db():
            await self._parse_data(weapon_data[0], weapon_data[1], weapon_data[2], weapon_data[3])


