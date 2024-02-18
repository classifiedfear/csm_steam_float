from aiogram.fsm.state import StatesGroup, State


class SettingStates(StatesGroup):
    GENERAL_SETTINGS = State()
    STATTRAK_SETTINGS = State()
    QUALITY_SETTINGS = State()
    SEARCH_STATE = State()
    canceling_state = State()


class OperationStates(StatesGroup):
    FIND_BY_USER_MSG = State()
    FIND_BY_DB = State()
    ADD_NEW_SKIN_TO_DB = State()
