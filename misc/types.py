from __future__ import annotations


class Iterable:
    def __init__(self, idx_limit: int):
        self.__current_idx, self.__idx_limit = 0, idx_limit

    @property
    def current_idx(self) -> int:
        return self.__current_idx

    def next(self):
        self.__current_idx = (self.__current_idx + 1) % self.__idx_limit

    def prev(self):
        self.__current_idx = (self.__current_idx - 1) % self.__idx_limit


class Resolution:
    def __init__(self, arg1: tuple[int, int] | int = 1, arg2: int = 1):
        self.width, self.height = arg1 if isinstance(arg1, tuple) else (arg1, arg2)

    def __str__(self) -> str:
        return '{}x{}'.format(self.width, self.height)

    def to_tuple(self) -> tuple[int, int]:
        return self.width, self.height
