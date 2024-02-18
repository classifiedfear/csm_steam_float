import pytest

from src.database_filler.cs_wiki.links.cs_wiki_link_creator import CsWikiLink
from src.misc.constants import tests_const
from src.misc.dto import SkinDTO


@pytest.mark.parametrize(
    ('skin_data', 'result'),
    (
        (SkinDTO('ak-47', 'asiimov', 'Factory New', True),
         tests_const.RESULT_CSM_WIKI_AK_47_LINK
         ),
        (SkinDTO('Desert Eagle', 'code Red', 'Field-Tested', False),
         tests_const.RESULT_CSM_WIKI_DESERT_EAGLE_LINK
         ),
    )
)
def test_should_create_link_for_csm_wiki(skin_data, result):
    link = CsWikiLink.create(skin_data)
    assert link == result
