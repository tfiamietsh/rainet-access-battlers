from functools import singledispatch


class Iterable:
    def __init__(self, idx_limit: int):
        self.__current_idx, self.__idx_limit = 0, idx_limit

    @property
    def current_idx(self):
        return self.__current_idx

    def next(self):
        self.__current_idx = (self.__current_idx + 1) % self.__idx_limit

    def prev(self):
        self.__current_idx = (self.__current_idx - 1) % self.__idx_limit


class Resolution:
    @singledispatch
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height

    @__init__.register
    def _(self, pair: tuple[int, int]):
        self.width, self.height = pair

    def __str__(self):
        return '{}x{}'.format(self.width, self.height)

    def to_tuple(self):
        return self.width, self.height
