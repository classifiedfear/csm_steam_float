from typing import List

from bs4 import BeautifulSoup


class CsgoDatabaseParser:
    @staticmethod
    def parse(response: str):
        soup = BeautifulSoup(response, 'lxml')
        item_boxes = soup.find_all('h3', class_='item-box-header')
        return CsgoDatabaseParser._find_weapons(item_boxes)

    @staticmethod
    def _find_weapons(item_boxes):
        result = []
        for item_box in item_boxes:
            result.append(item_box.text.strip())
        return result


class SkinCsgoDatabaseParser:
    @staticmethod
    def parse(response: str):
        soup = BeautifulSoup(response, 'lxml')
        skin_box_headers = soup.find_all('div', class_='skin-box-header')
        return SkinCsgoDatabaseParser._find_skin_name(skin_box_headers)

    @staticmethod
    def _find_skin_name(skin_box_headers: List[BeautifulSoup]):
        result = []
        for header in skin_box_headers:
            weapon, part, skin = header.text.partition('|')
            result.append(skin.strip())
        return result
