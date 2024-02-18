import dataclasses


@dataclasses.dataclass
class UserSettingsDTO:
    stattrak: bool
    quality: str
    search: bool