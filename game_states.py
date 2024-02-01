import pygame
from abc import ABC, abstractmethod


class GameState(ABC):
    __game = None

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, game):
        self.__game = game

    @abstractmethod
    def mouse_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def keyboard_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self):
        pass
