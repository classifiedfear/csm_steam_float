import pytest

from src.misc.dto import SkinDTO
from src.misc.exceptions import InvalidSkin, InvalidWeapon
from src.telegram_bot.msg_parser import MsgParser


@pytest.fixture()
def msg_parser():
    return MsgParser()


def test_should_get_skin_dto_from_full_string(msg_parser):
    skin_dto = msg_parser.execute('pp-bizon, CODE RED, STATTRAK, FACTORY NEW')
    assert isinstance(skin_dto, SkinDTO)


def test_should_raise_invalid_skin(msg_parser):
    with pytest.raises(InvalidSkin):
        msg_parser.execute('pp-bizon, stattrak')


def test_should_raise_invalid_weapon(msg_parser):
    with pytest.raises(InvalidWeapon):
        msg_parser.execute('code red')


def test_should_get_skin_dto_with_default_quality(msg_parser):
    skin_dto = msg_parser.execute('code red, desert eagle', quality_default='Well Worn')
    assert skin_dto.quality == 'Well Worn'


def test_should_get_skin_dto_with_default_stattrak_status(msg_parser):
    skin_dto = msg_parser.execute('ak-47, asiimov', stattrak_default=True)
    assert skin_dto.stattrak is True