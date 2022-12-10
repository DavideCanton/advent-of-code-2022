import sys
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import TextIO


class BaseAdventDay(metaclass=ABCMeta):
    def load_asset(self, name) -> TextIO:
        module = sys.modules[self.__module__]
        asset: Path = Path(module.__file__).parent / "data" / name
        return asset.open()

    @abstractmethod
    def get_input(self, variant) -> tuple:
        pass

    def run(self, variant):
        method = getattr(self, f"run_{variant}")
        return method(*self.get_input(variant))


class SameComputationAdventDay(BaseAdventDay, metaclass=ABCMeta):
    @abstractmethod
    def compute(self, var, *input):
        pass

    def run(self, variant):
        input = self.get_input(variant)
        return self.compute(variant, *input)
