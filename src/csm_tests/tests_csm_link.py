import pytest

from src.csm.links.csm_link_creator import CsmLinkCreator
from src.csm.links.csm_skin_link_creator import CsmSkinLinkCreator
from src.misc.constants import tests_const
from src.misc.dto import SkinDTO


@pytest.mark.parametrize(
    ('skin_dto', 'result'),
    (
        (SkinDTO('AK-47', 'Asiimov', 'Field-Tested', False), tests_const.RESULT_CSM_AK_47_LINK),
        (SkinDTO('Desert Eagle', 'Code Red', 'Battle-Scarred', True), tests_const.RESULT_CSM_DESERT_EAGLE_LINK),
    )
)
def test_should_create_link_for_csm(skin_dto, result):
    link = CsmLinkCreator.create(skin_dto)
    assert link == result


def test_should_change_offset_in_link():
    link = CsmLinkCreator.create(SkinDTO('AK-47', 'Asiimov', 'Field-Tested', False))
    first_offset_result = link.find('offset=0')
    link = CsmLinkCreator.create(SkinDTO('AK-47', 'Asiimov', 'Field-Tested', False), offset=60)
    second_offset_result = link.find('offset=60')

    assert first_offset_result != -1
    assert second_offset_result != -1


def test_should_create_link_for_current_skin():
    link = CsmSkinLinkCreator.create()
    assert link == tests_const.RESULT_CSM_SPECIFIC_SKIN_LINK

