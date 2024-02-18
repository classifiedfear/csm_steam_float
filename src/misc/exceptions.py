class Error(Exception):
    """Base class for all bot exception"""


class InvalidWeapon(Exception):
    """Wrong weapon name"""


class InvalidSkin(Exception):
    """Wrong skin name"""


class StatTrakError(Exception):
    """Wrong type StatTrak"""


class RequestError(Exception):
    """Request error"""


class TechError(Exception):
    """Resource didn't load error"""
