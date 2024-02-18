from enum import Enum

FACTORY_NEW = 'Factory New'
MINIMAL_WEAR = 'Minimal Wear'
FIELD_TESTED = 'Field-Tested'
WELL_WORN = 'Well-Worn'
BATTLE_SCARRED = 'Battle-Scarred'


class Qualities(Enum):
    FACTORY_NEW = {'num': 1, 'str': 'Factory New'}
    MINIMAL_WEAR = {'num': 2, 'str': 'Minimal Wear'}
    FIELD_TESTED = {'num': 3, 'str': 'Field-Tested'}
    WELL_WORN = {'num': 4, 'str': 'Well-Worn'}
    BATTLE_SCARRED = {'num': 5, 'str': 'Battle-Scarred'}

    def __init__(self, vals):
        self.num = vals['num']
        self.str = vals['str']





