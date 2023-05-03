import pygame
import rainet


class AnimatedImage:
    def __init__(self, image, frame_indices, delay_ms):
        max_i, max_j = 0, 0
        image_size = image.get_size()
        for i, j in frame_indices:
            max_i, max_j = max(max_i, i), max(max_j, j)
        frame_size = image_size[0] // (max_j + 1), image_size[1] // (max_i + 1)

        self._frames = []
        for i, j in frame_indices:
            self._frames.append(image.subsurface((j * frame_size[0], i * frame_size[1], *frame_size)))
        self._current_frame = 0
        self._clock = pygame.time.Clock()
        self._delay_ms = delay_ms
        self._prev_ticks = pygame.time.get_ticks()
        self._visibility = True

    def set_visibility(self, visibility):
        self._visibility = visibility

    def draw(self, pos):
        if self._visibility:
            curr_ticks = pygame.time.get_ticks()

            rainet.RaiNet.screen.blit(self._frames[self._current_frame], pos)
            if curr_ticks - self._prev_ticks >= self._delay_ms:
                self._prev_ticks = curr_ticks
                self._current_frame = (self._current_frame + 1) % len(self._frames)
