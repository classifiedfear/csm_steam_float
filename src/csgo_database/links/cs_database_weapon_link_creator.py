from src.misc.link_tools import LinkBuilder


class CsgoDatabaseWeaponsLinkCreator:
    @staticmethod
    def create():
        return (
            LinkBuilder('https://www.csgodatabase.com/')
            .add_part_link('weapons/').build()
        )


class CsgoDatabaseSkinsLinkCreator:
    @staticmethod
    def create(weapon: str):
        return (
            LinkBuilder('https://www.csgodatabase.com/')
            .add_part_link('weapons/')
            .add_part_link(weapon.lower().replace(' ', '-')).build()
        )
print(CsgoDatabaseWeaponsLinkCreator.create())