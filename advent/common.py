from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import TextIO


def load_asset(module, name) -> TextIO:
    asset: Path = Path(module).parent / "data" / name
    return asset.open()


class BaseAdventDay(metaclass=ABCMeta):
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
