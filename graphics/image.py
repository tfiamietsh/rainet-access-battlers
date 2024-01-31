from __future__ import annotations
from pathlib import Path
import pygame
import PIL.Image
from misc.types import Vec2f, Iterable
from misc.decorators import delayed


class Image:
    def __init__(self, pil_image: PIL.Image):
        self.__pil_image, self.__size = pil_image, Vec2f(pil_image.size)
        self.__image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode).convert_alpha()

    @property
    def size(self) -> Vec2f:
        return self.__size

    def resized(self, scale_factor: Vec2f) -> Image:
        return Image(self.__pil_image.resize((scale_factor * self.__size).to_tuple()))

    def rotated(self, angle: float = 180) -> Image:
        return Image(self.__pil_image.rotate(angle))

    def draw(self, surface: pygame.Surface, pos: Vec2f):
        surface.blit(self.__image, pos.to_tuple())


class ImageLoader:
    @staticmethod
    def load(path: Path) -> Image:
        return Image(PIL.Image.open(path))


class AnimatedImage(Iterable):
    def __init__(self, frames: list[Image], delay_between_ms: int, delay_after_ms: int):
        super().__init__(len(frames))
        self.__frames = frames
        self.__delay_between_ms, self.__delay_after_ms = delay_between_ms, delay_after_ms
        AnimatedImage.draw = delayed(self.__delay, self.next)(AnimatedImage.draw)

    def __delay(self) -> int:
        return self.__delay_after_ms if self._current_idx == self._idx_limit - 1 else self.__delay_between_ms

    @property
    def size(self) -> Vec2f:
        return self.__frames[0].size

    @property
    def current_frame(self) -> Image:
        return self.__frames[self._current_idx]

    def resized(self, scale_factor: Vec2f) -> AnimatedImage:
        return AnimatedImage([frame.resized(scale_factor) for frame in self.__frames],
                             self.__delay_between_ms, self.__delay_after_ms)

    def draw(self, surface: pygame.Surface, pos: Vec2f):
        self.current_frame.draw(surface, pos)
