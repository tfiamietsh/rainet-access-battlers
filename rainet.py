import pygame
import pygame.event


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('RaiNet Access Battlers')
        self.__game_over = False
        self.__screen = pygame.display.set_mode((1, 1))
        self.__FPS = 30
        self.__clock = pygame.time.Clock()

    def __del__(self):
        pygame.quit()

    @property
    def screen(self):
        return self.__screen

    def start(self):
        while not self.__game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_over = True
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP and \
                        event.button == pygame.BUTTON_LEFT:
                    #   TODO: mouse event
                    pass
                elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    #   TODO: keyboard event
                    pass
            self.screen.fill('black')
            #   TODO: update event
            pygame.display.flip()
            self.__clock.tick(self.__FPS)


if __name__ == '__main__':
    game = Game()
    game.start()
