import pygame
from misc import utils
from misc.constants import *
from graphics import ui, animation
from network import bt
import rainet
from math import ceil
from functools import partial


class MainMenu(ui.Menu):
    def __init__(self, on_click_new_duel, on_click_options, on_click_exit_game):
        jp_font = ui.Font(80, is_jp=True)
        non_jp_font = ui.Font()

        super().__init__()
        super()._add_label(ui.Label(jp_font, '     雷ネット', (50, 250)))
        super()._add_label(ui.Label(jp_font, 'アクセスバトラーズ', (50, 330)))
        super()._add_button(ui.Button(non_jp_font, 'BT PARTY', (80, 600, 400, 55), on_click_new_duel, fx=True))
        super()._add_button(ui.Button(non_jp_font, 'OPTIONS', (80, 680, 400, 55), on_click_options, fx=True))
        super()._add_button(ui.Button(non_jp_font, 'EXIT GAME', (80, 760, 400, 65), on_click_exit_game, fx=True))


class StyleSelectionMenu(ui.Menu):
    def __init__(self, on_click_done, on_click_main_menu):
        font = ui.Font()

        self._style = 0
        self._styles = []
        for style in range(NUM_STYLES):
            style_image_size = 2 * CARD_SIZE[0], 2 * CARD_SIZE[1]
            style_image = pygame.surface.Surface(style_image_size).convert_alpha()

            pygame.transform.scale(rainet.RaiNet.img.subsurface((*CARD_STYLES_OFFSETS['h'][style],
                                                                 *CARD_SIZE)), style_image_size, style_image)
            self._styles.append(style_image)
        super().__init__()
        super()._add_button(ui.Button(font, 'BACK', (50, 50, 400, 60), on_click_main_menu, fx=True))
        super()._add_label(ui.Label(font, 'Select Color', (280, 250)))
        super()._add_image(ui.Image(self._styles[0], (330, 350)))
        super()._add_button(ui.Button(font, '←', (260, 400, 50, 55), self._on_change_style_left))
        super()._add_button(ui.Button(font, '→', (480, 400, 50, 55), self._on_change_style_right))
        super()._add_button(ui.Button(font, 'DUEL ACCESS!', (265, 550, 255, 60), on_click_done))

    def __call__(self):
        return self._style

    def _on_change_style_left(self):
        self._style = utils.cyclic_decrement(self._style, NUM_STYLES)
        self._images[1].set_image(self._styles[self._style])

    def _on_change_style_right(self):
        self._style = utils.cyclic_increment(self._style, NUM_STYLES)
        self._images[1].set_image(self._styles[self._style])


class Options(ui.Menu):
    def __init__(self, on_click_main_menu):
        font = ui.Font()

        self._bgm_volume = utils.round(int(100 * pygame.mixer.Channel(0).get_volume()), 5)
        self._sfx_volume = utils.round(int(100 * pygame.mixer.Channel(1).get_volume()), 5)
        super().__init__()
        super()._add_button(ui.Button(font, 'DONE', (80, 450, 400, 60), on_click_main_menu, fx=True))
        super()._add_label(ui.Label(font, 'BGM VOLUME', (100, 150)))
        super()._add_label(ui.Label(font, utils.correct_percent_str(self._bgm_volume), (600, 150)))
        super()._add_button(ui.Button(font, '-', (550, 150, 25, 55), self._on_bgm_volume_down))
        super()._add_button(ui.Button(font, '+', (690, 150, 25, 55), self._on_bgm_volume_up))
        super()._add_label(ui.Label(font, 'SFX VOLUME', (100, 250)))
        super()._add_label(ui.Label(font, utils.correct_percent_str(self._sfx_volume), (600, 250)))
        super()._add_button(ui.Button(font, '-', (550, 250, 25, 55), self._on_sfx_volume_down))
        super()._add_button(ui.Button(font, '+', (690, 250, 25, 55), self._on_sfx_volume_up))

    def _on_bgm_volume_up(self):
        if self._bgm_volume < 100:
            self._bgm_volume += 5
        self._labels[1].set_text(utils.correct_percent_str(self._bgm_volume))
        pygame.mixer.Channel(0).set_volume(self._bgm_volume / 100.)

    def _on_bgm_volume_down(self):
        if self._bgm_volume > 0:
            self._bgm_volume -= 5
        self._labels[1].set_text(utils.correct_percent_str(self._bgm_volume))
        pygame.mixer.Channel(0).set_volume(self._bgm_volume / 100)

    def _on_sfx_volume_up(self):
        if self._sfx_volume < 100:
            self._sfx_volume += 5
        self._labels[3].set_text(utils.correct_percent_str(self._sfx_volume))
        pygame.mixer.Channel(1).set_volume(self._sfx_volume / 100)

    def _on_sfx_volume_down(self):
        if self._sfx_volume > 0:
            self._sfx_volume -= 5
        self._labels[3].set_text(utils.correct_percent_str(self._sfx_volume))
        pygame.mixer.Channel(1).set_volume(self._sfx_volume / 100)


class Message(ui.Menu):
    def __init__(self, text, text_x_offset, on_click_ok):
        font = ui.Font()

        super().__init__()
        super()._add_label(ui.Label(font, text, (text_x_offset, 400)))
        super()._add_button(ui.Button(font, 'OK', (375, 500, 50, 60), on_click_ok))


class WaitingForConnectionMenu(ui.Menu):
    def __init__(self, on_click_back, on_join_second_player, on_connection_error):
        font = ui.Font()

        super().__init__()
        super()._add_button(ui.Button(font, 'BACK', (50, 50, 400, 60), self._back, fx=True))
        super()._add_label(ui.Label(font, 'Device name:', (50, 740)))
        super()._add_label(ui.Label(font, bt.get_device_name(), (50, 800)))
        super()._add_label(ui.Label(font, 'Waiting for the second player to join', (50, 380)))
        self._spinner_pos = (370, 455)
        self._spinner = animation.AnimatedImage(rainet.RaiNet.img.subsurface(SPINNER_RECT),
                                                frame_indices=SPINNER_FRAME_INDICES, delay_ms=100)
        self._on_click_back = on_click_back
        self._on_join_second_player = on_join_second_player
        self._on_connection_error = on_connection_error
        self._server = None
        self._wait_connection_thread = None

    def __call__(self):
        return self._server

    def wait_for(self):
        self._server = bt.Server()
        utils.start_daemon_thread(self._thread_function)

    def update(self):
        super().update()
        self._spinner.draw(self._spinner_pos)

    def _thread_function(self):
        e = self._server.wait_for_connection()
        if e is None:
            if self._server.send(SECRET_KEY) is None and self._server.recv() == SECRET_KEY:
                self._on_join_second_player()
            else:
                self._on_connection_error()
        else:
            self._server.close()

    def _back(self):
        self._server.close()
        self._on_click_back()


class DeviceSelectionMenu(ui.Menu):
    _num_devices_per_page = 5

    def __init__(self, on_click_back, on_connect_to_server, on_connection_cannot):
        font = ui.Font()
        height = 320

        super().__init__()
        super()._add_label(ui.Label(font, 'Select Device to Connect', (150, 230)))
        for i in range(self._num_devices_per_page):
            super()._add_button(ui.Button(font, '', (150, height, 490, 60), lambda: True, visibility=False))
            height += 70
        height += 20
        super()._add_button(ui.Button(font, 'BACK', (50, 50, 400, 60), on_click_back, fx=True))
        super()._add_button(ui.Button(font, 'PREV', (410, height, 100, 55), self._prev_page))
        super()._add_button(ui.Button(font, 'NEXT', (540, height, 100, 55), self._next_page))
        super()._add_image(ui.Image(rainet.RaiNet.img.subsurface((1760, 69, 64, 69)), (140, height - 20)))
        super()._add_button(ui.Button(font, ' ', (150, height, 48, 48), self._start_discovering))
        self._spinner_pos = (370, 455)
        self._spinner = animation.AnimatedImage(rainet.RaiNet.img.subsurface(SPINNER_RECT),
                                                frame_indices=SPINNER_FRAME_INDICES, delay_ms=100)
        self._spinner.set_visibility(False)
        self._on_connect_to_server = on_connect_to_server
        self._on_connection_cannot = on_connection_cannot
        self._client = None
        self._start_discovering()

    def __call__(self):
        return self._client

    def update(self):
        super().update()
        self._spinner.draw(self._spinner_pos)

    def _on_select_server(self, server_addr):
        self._client = bt.Client()
        utils.start_daemon_thread(self._thread_function, (server_addr,))

    def _thread_function(self, server_addr):
        e = self._client.connect(server_addr)

        if e is None and self._client.send(SECRET_KEY) is None and self._client.recv() == SECRET_KEY:
            self._on_connect_to_server()
        else:
            self._on_connection_cannot()

    def _start_discovering(self):
        utils.start_daemon_thread(self._discover_devices)

    def _discover_devices(self):
        self._buttons[-1].set_visibility(False)
        self._images[-1].set_visibility(False)
        self._spinner.set_visibility(True)
        for i in range(5):
            self._buttons[i].set_visibility(False)
        self._device_names = bt.discover_devices()
        if isinstance(self._device_names, Exception):
            self._device_names = []
        self._current_page = 0
        self._refresh_buttons()
        self._num_pages = int(ceil(len(self._device_names) / self._num_devices_per_page))

    def _next_page(self):
        self._current_page = utils.cyclic_increment(self._current_page, self._num_pages)
        self._refresh_buttons()

    def _prev_page(self):
        self._current_page = utils.cyclic_decrement(self._current_page, self._num_pages)
        self._refresh_buttons()

    def _refresh_buttons(self):
        offset_idx = self._num_devices_per_page * self._current_page
        device_names = self._device_names[offset_idx:offset_idx + self._num_devices_per_page]

        for i, (addr, name) in enumerate(device_names):
            self._buttons[i].get_label().set_text(name[:25] if len(name) > 0 else '*unnamed device*')
            self._buttons[i].set_func(partial(self._on_select_server, addr))
            self._buttons[i].set_visibility(True)
        for i in range(len(device_names), 5):
            self._buttons[i].set_visibility(False)
        self._buttons[-1].set_visibility(True)
        self._images[-1].set_visibility(True)
        self._spinner.set_visibility(False)


class RoleSelectionMenu(ui.Menu):
    def __init__(self, on_click_back, on_new_duel, on_join_duel):
        title_font = ui.Font()
        font = ui.Font(40)

        super().__init__()
        super()._add_button(ui.Button(title_font, 'BACK', (50, 50, 400, 60), on_click_back, fx=True))
        super()._add_label(ui.Label(font, 'Make sure that bluetooth is turned on on this device', (80, 350)))
        super()._add_label(ui.Label(font, 'and on the device of second player', (180, 400)))
        super()._add_button(ui.Button(title_font, 'NEW DUEL', (100, 500, 190, 60), on_new_duel))
        super()._add_button(ui.Button(title_font, 'JOIN DUEL', (480, 500, 190, 60), on_join_duel))
