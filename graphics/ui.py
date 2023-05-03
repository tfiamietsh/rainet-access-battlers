import pygame
import pygame.gfxdraw
from misc.constants import BGI_OFFSETS, FIELD_SIZE, ACTION_SFX
import re
from misc import utils
import rainet


class Image:
    def __init__(self, image, pos):
        self._image = image
        self._pos = pos
        self._visibility = True

    def set_visibility(self, visibility):
        self._visibility = visibility

    def set_image(self, image):
        self._image = image

    def get_image(self):
        return self._image

    def update(self):
        if self._visibility:
            rainet.RaiNet.screen.blit(self._image, self._pos)


class Font:
    def __init__(self, size=60, is_jp=False):
        self._font = pygame.font.Font(rainet.RaiNet.jp_font_path if is_jp else rainet.RaiNet.non_jp_font_path, size)

    def print(self, text, pos, color=(255, 255, 255)):
        rainet.RaiNet.screen.blit(self._font.render(text, False, (0, 0, 0)), (pos[0] + 2, pos[1] + 2))
        rainet.RaiNet.screen.blit(self._font.render(text, False, color), pos)


class Label:
    def __init__(self, font, text, pos):
        self._font = font
        self._text = text
        self._pos = pos

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def update(self):
        self._font.print(self._text, self._pos)


class Button:
    def __init__(self, font, text, rect, func, fx=False, visibility=True):
        self._label = Label(font, text, (rect[0], rect[1]))
        self._rect = rect
        self._func = func
        self._padding = 10
        self._fx = fx
        self._visibility = visibility

    def set_func(self, func):
        self._func = func

    def set_visibility(self, visibility):
        self._visibility = visibility

    def get_label(self):
        return self._label

    def update(self, mouse_pos):
        padded_rect = (self._rect[0] - self._padding, self._rect[1] - self._padding,
                       self._rect[2] + 2 * self._padding, self._rect[3])

        if self._visibility:
            if utils.is_pos_in_rect(mouse_pos, padded_rect):
                pygame.gfxdraw.box(rainet.RaiNet.screen, pygame.Rect(*padded_rect), (0, 0, 0, 127))
                if self._fx:
                    self._label.set_text(f'>{self._label.get_text()}<')
            self._label.update()
            self._label.set_text(re.sub('[><]', '', self._label.get_text()))

    def on_mouse_btn_up(self, mouse_pos):
        if utils.is_pos_in_rect(mouse_pos, (self._rect[0] - self._padding, self._rect[1] - self._padding,
                                            self._rect[2] + 2 * self._padding, self._rect[3] + 2 * self._padding))\
                and self._visibility:
            rainet.RaiNet.play_sound(ACTION_SFX)
            self._func()


class Menu:
    def __init__(self):
        self._buttons = []
        self._labels = []
        self._images = [Image(rainet.RaiNet.img.subsurface((*BGI_OFFSETS, *FIELD_SIZE)), (0, 0))]

    def _add_button(self, button):
        self._buttons.append(button)

    def _add_label(self, label):
        self._labels.append(label)

    def _add_image(self, image):
        self._images.append(image)

    def on_mouse_btn_up(self):
        mouse_pos = pygame.mouse.get_pos()

        for button in self._buttons:
            button.on_mouse_btn_up(mouse_pos)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self._images[0].update()
        for button in self._buttons:
            button.update(mouse_pos)
        for image in self._images[1:]:
            image.update()
        for label in self._labels:
            label.update()
