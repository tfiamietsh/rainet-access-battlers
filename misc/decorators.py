from __future__ import annotations
from typing import Callable

import pygame.time


def singleton(cls: type):
    def wrapper(*args: tuple[any, ...], **kwargs: dict[str, any]):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]
    __instances = {}
    return wrapper


def delayed(delay: int | Callable[[], int], delayed_func: Callable[[], None]):
    def decorator(func: Callable[[any, ...], any]):
        def wrapper(*args: tuple[any, ...], **kwargs: dict[str, any]):
            nonlocal __then
            now = pygame.time.get_ticks()
            if now - __then >= (delay if isinstance(delay, int) else delay()):
                __then = now
                delayed_func()
            func(*args, **kwargs)
        __then = pygame.time.get_ticks()
        return wrapper
    return decorator
