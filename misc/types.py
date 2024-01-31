from __future__ import annotations
from typing import Callable


class Iterable:
    def __init__(self, idx_limit: int):
        self._current_idx, self._idx_limit = 0, idx_limit

    def next(self):
        self._current_idx = (self._current_idx + 1) % self._idx_limit

    def prev(self):
        self._current_idx = (self._current_idx - 1) % self._idx_limit


class Resolution:
    def __init__(self, arg1: tuple[int, int] | int = 1, arg2: int = 1):
        self.width, self.height = arg1 if isinstance(arg1, tuple) else (arg1, arg2)

    def __str__(self) -> str:
        return '{}x{}'.format(self.width, self.height)

    def to_tuple(self) -> tuple[int, int]:
        return self.width, self.height


class Vec2f:
    def __init__(self, arg1: tuple[float, float] | float = 0., arg2: float = 0.):
        self.x, self.y = arg1 if isinstance(arg1, tuple) else (arg1, arg2)

    def __apply(self, func: Callable[[float, float], float | bool], other: Vec2f | tuple[float, float] | float | int,
                return_bool: bool = False) -> Vec2f | bool:
        result, args = Vec2f(), 'xy'
        if isinstance(other, Vec2f):
            other = other.__dict__
        elif isinstance(other, tuple):
            other = {arg: other[i] for i, arg in enumerate(args)}
        elif isinstance(other, (float, int)):
            other = {arg: other for arg in args}
        for arg in args:
            result.__dict__[arg] = func(self.__dict__[arg], other[arg])
        return all([result.__dict__[arg] for arg in args]) if return_bool else result

    def __add__(self, other: Vec2f | tuple[float, float] | float | int) -> Vec2f:
        return self.__apply(lambda a, b: a + b, other)

    def __sub__(self, other: Vec2f | tuple[float, float] | float | int) -> Vec2f:
        return self.__apply(lambda a, b: a - b, other)

    def __mul__(self, other: Vec2f | tuple[float, float] | float | int) -> Vec2f:
        return self.__apply(lambda a, b: a * b, other)

    def __truediv__(self, other: Vec2f | tuple[float, float] | float | int) -> Vec2f:
        return self.__apply(lambda a, b: a / b, other)

    def __le__(self, other: Vec2f | tuple[float, float] | float | int) -> bool:
        return self.__apply(lambda a, b: a <= b, other, True)

    def __ge__(self, other: Vec2f | tuple[float, float] | float | int) -> bool:
        return self.__apply(lambda a, b: a >= b, other, True)

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y
