import pygame
from misc.constants import *
from mechanics import duel, agent
from graphics import menus
from network import bt
from misc import utils

__DEBUG__MODE__ = False

pygame.mixer.init()
pygame.init()
pygame.font.init()


class RaiNet:
    screen = pygame.display.set_mode(tuple(FIELD_SIZE))
    img = pygame.image.load('data/images/image0.png').convert_alpha()
    inv_img = pygame.transform.flip(img.copy(), True, True)
    non_jp_font_path = 'data/fonts/font0.ttf'
    jp_font_path = 'data/fonts/font1.ttf'
    _sfx = {
        ACTION_SFX: pygame.mixer.Sound('data/sounds/sound1.wav'),
        DUEL_END_SFX: pygame.mixer.Sound('data/sounds/sound2.wav'),
        SKILL_SFX: pygame.mixer.Sound('data/sounds/sound3.wav')
    }

    def __init__(self):
        self._game_over = False
        self._stages = {
            MAIN_MENU: menus.MainMenu(self._select_role, self._open_options, self._exit_game),
            ROLE_SELECTION: menus.RoleSelectionMenu(self._open_main_menu, self._new_duel, self._join_duel),
            STYLE_SELECTION: menus.StyleSelectionMenu(self._start_duel, self._open_main_menu),
            CONNECTION_ERROR: menus.Message('CONNECTION ERROR', 220, self._select_role),
            CONNECTION_CANNNOT: menus.Message('CONNECTION CANNOT BE ESTABLISHED', 50, self._join_duel),
            CONNECTION_LOST: menus.Message('CONNECTION IS LOST', 200, self._open_main_menu),
            NEW_DUEL: None,
            JOIN_DUEL: None,
            DUEL: None,
            DUEL_END: None,
            OPTIONS: None
        }
        self._current_stage = MAIN_MENU
        self._connection = None
        pygame.display.set_caption('Rai-Net Access Battlers')
        pygame.display.set_icon(RaiNet.img.subsurface(600, 0, 64, 64))
        pygame.mixer.Channel(0).set_volume(.25)
        pygame.mixer.Channel(1).set_volume(.5)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/sounds/sound0.wav'), loops=-1)

    @classmethod
    def play_sound(cls, sfx):
        pygame.mixer.Channel(1).play(RaiNet._sfx[sfx])

    def _open_main_menu(self):
        self._current_stage = MAIN_MENU

    def _select_role(self):
        self._current_stage = ROLE_SELECTION

    def _new_duel(self):
        if bt.is_bluetooth_enabled():
            self._stages[NEW_DUEL] = menus.WaitingForConnectionMenu(self._select_role, self._select_style,
                                                                    self._on_connection_error)
            self._current_stage = NEW_DUEL
            self._stages[self._current_stage].wait_for()

    def _join_duel(self):
        if bt.is_bluetooth_enabled():
            self._stages[JOIN_DUEL] = menus.DeviceSelectionMenu(self._select_role, self._select_style,
                                                                self._on_connection_cannot)
            self._current_stage = JOIN_DUEL

    def _select_style(self):
        self._connection, self._current_stage = self._stages[self._current_stage](), STYLE_SELECTION

    def _start_duel(self):
        p1_style = self._stages[STYLE_SELECTION]()

        def send_recv():
            self._connection.send(str(p1_style))
            return int(self._connection.recv())

        p2_style = utils.try_else(send_recv, self._on_connection_lost)
        if isinstance(p2_style, int):
            self._stages[DUEL], self._current_stage = duel.Duel(p1_style, p2_style, self._connection, self._end_duel,
                                                                self._on_connection_lost), DUEL

    def _end_duel(self, pl):
        RaiNet.play_sound(DUEL_END_SFX)
        message = {P1: ('YOU WON!', 310), P2: ('YOU LOST!', 300)}[pl]
        self._connection.close()
        self._stages[DUEL_END], self._current_stage = menus.Message(*message, self._open_main_menu), DUEL_END

    def _open_options(self):
        self._stages[OPTIONS], self._current_stage = menus.Options(self._open_main_menu), OPTIONS

    def _exit_game(self):
        self._game_over = True

    def _on_connection_error(self):
        self._connection.close()
        self._current_stage = CONNECTION_ERROR

    def _on_connection_lost(self):
        self._connection.close()
        self._current_stage = CONNECTION_LOST

    def _on_connection_cannot(self):
        self._connection.close()
        self._current_stage = CONNECTION_CANNNOT

    def update(self):
        while not self._game_over:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self._stages[self._current_stage].on_mouse_btn_up()
                if event.type == pygame.MOUSEMOTION:
                    if self._current_stage == DUEL:
                        self._stages[DUEL].on_mouse_move()
                if event.type == pygame.QUIT:
                    self._game_over = True
            self._stages[self._current_stage].update()
            pygame.display.flip()


if __name__ == '__main__':
    game = RaiNet()
    game.update()
