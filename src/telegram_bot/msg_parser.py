from typing import List, Dict, Any

from src.misc.dto import SkinDTO
from src.misc.exceptions import InvalidWeapon, InvalidSkin
from src.telegram_bot.resources.constants import skin_const


class MsgParser:
    _WEAPONS = skin_const.Weapons
    _QUALITIES = skin_const.Qualities

    def get_skin_dto(
            self,
            msg: str,
            stattrak_default: bool = False,
            quality_default: str = skin_const.Qualities.FIELD_TESTED.value
    ) -> SkinDTO:
        values = self._get_weapon_values_from_user_msg(msg)
        return self._get_handled_parsed_values(values, stattrak_default, quality_default)

    def _get_weapon_values_from_user_msg(self, msg: str) -> Dict[str, str | bool]:
        lower_and_strip_values = self._get_lower_and_strip_values(msg)
        return self._collect_values_from_msg(lower_and_strip_values)

    @staticmethod
    def _get_handled_parsed_values(
            values: Dict[str, str | bool],
            stattrak_default: bool = False,
            quality_default: str = skin_const.Qualities.FIELD_TESTED.value
    ):
        if not (weapon := values.get('weapon')):
            raise InvalidWeapon

        if not (skin := values.get('skin')):
            raise InvalidSkin

        if not (quality := values.get('quality')):
            quality = quality_default

        if not (stattrak := values.get('stattrak')):
            stattrak = stattrak_default

        return SkinDTO(weapon, skin, quality, stattrak)

    @staticmethod
    def _get_lower_and_strip_values(msg: str) -> List[str]:
        return [msg_part.strip() for msg_part in msg.lower().split(',')]

    def _collect_values_from_msg(self, lower_and_strip_values: List[str]) -> Dict[str, Any]:
        values = {}
        while lower_and_strip_values:
            msg_part = lower_and_strip_values.pop()
            if msg_part in self._WEAPONS.get_weapons_in_lower_case():
                values['weapon'] = self._WEAPONS.get_correct_weapon_name(msg_part)
            elif msg_part in self._QUALITIES.get_qualities_in_lower_case():
                values['quality'] = self._QUALITIES.get_correct_quality_name(msg_part)
            elif msg_part == 'stattrak':
                values['stattrak'] = True
            else:
                values['skin'] = msg_part.title()
        return values




