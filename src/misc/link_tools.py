from typing import Self


class LinkBuilder:
    def __init__(self, link_root: str):
        self._link_root = link_root
        self._link_result = link_root
        self._is_question_mark_appended = False

    def change_link_root(self, new_link_root: str) -> Self:
        self._link_root = new_link_root
        self.reset()
        return self

    def add_param(self, key: str, value: str) -> Self:
        self._link_result += '?' if not self._is_question_mark_appended else '&'
        self._is_question_mark_appended = True
        self._link_result += f'{key}={value}'
        return self

    def add_part_link(self, part: str) -> Self:
        self._link_result += part
        return self

    def build(self) -> str:
        self._is_question_mark_appended = False
        result = self._link_result
        self._link_result = self._link_root
        return result

    def reset(self) -> Self:
        self._link_result = self._link_root
        return self


class Pager:
    def __init__(self, page_size: int):
        self._page_size = page_size
        self._current_page = 0

    @property
    def get_current_page(self):
        return self._current_page

    @property
    def page_size(self):
        return self._page_size

    @property
    def offset(self):
        return self._current_page * self._page_size

    def get_next_offset(self):
        offset = self.offset
        self._current_page += 1
        return offset

    def reset_page(self):
        self._current_page = 0
