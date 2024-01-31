from __future__ import annotations
import pygame
import PIL.Image
from misc.types import Vec2f


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
