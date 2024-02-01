from __future__ import annotations
from misc.types import *
from graphics.image import Image, AnimatedImage


class ResolutionManager(dict, Iterable):
    def __init__(self, default_resolution: Resolution, resolutions: list[Resolution]):
        dict.__init__(self, {i: resolution for i, resolution in enumerate(resolutions)})
        Iterable.__init__(self, len(resolutions))
        self.__default_resolution = default_resolution

    @property
    def default_resolution(self) -> Resolution:
        return self.__default_resolution

    @property
    def current_resolution(self) -> Resolution:
        return self[self._current_idx]


class ImageManager(dict):
    def __init__(self, resolution_manager: ResolutionManager):
        super().__init__(self)
        default_resolution_scale_factor = Vec2f(resolution_manager.default_resolution.to_tuple())
        self.__resolution_manager = resolution_manager
        self.__resolution_scale_factor_map = {
            resolution: Vec2f(resolution.to_tuple()) / default_resolution_scale_factor
            for resolution in resolution_manager.values()
        }

    def __setitem__(self, name: str, image: Image | AnimatedImage):
        super().__setitem__(name, {
            resolution: image.resized(scale_factor)
            for resolution, scale_factor in self.__resolution_scale_factor_map.items()
        })

    def __getitem__(self, name: str) -> Image | AnimatedImage:
        return super().__getitem__(name)[self.__resolution_manager.current_resolution]

    @property
    def resolution_manager(self) -> ResolutionManager:
        return self.__resolution_manager
