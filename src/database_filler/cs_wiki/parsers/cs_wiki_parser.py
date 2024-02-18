from typing import List

from bs4 import BeautifulSoup



class CsWikiParser:
    @staticmethod
    def parse(response: str):
        return CsWikiParser._find_skin(response)

    @staticmethod
    def _find_skin(response: str):
        soup = BeautifulSoup(response, 'lxml')
        name = CsWikiParser._find_skin_name(soup)
        qualities = CsWikiParser._find_qualities(soup)
        stattraks = CsWikiParser._find_stattraks(soup)
        return {'name': name, 'qualities': qualities, 'stattraks': stattraks}

    @staticmethod
    def _find_stattraks(soup: BeautifulSoup) -> int:
        result = [text for item in soup.find_all('td') if (text := item.get_text()) != '']
        if 'StatTrak™' in result:
            return 1
        return 0

    @staticmethod
    def _find_qualities(soup: BeautifulSoup):
        return [text for item in soup.find_all('th') if (text := item.get_text()) != '']

    @staticmethod
    def _find_skin_name(soup: BeautifulSoup):
        return soup.find('title').text


