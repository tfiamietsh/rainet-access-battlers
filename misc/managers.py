from misc.types import *


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
        return self[self.current_idx]
