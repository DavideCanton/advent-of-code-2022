from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TextIO


@dataclass
class BaseAdventDay(metaclass=ABCMeta):
    day: ClassVar[int]
    input_folder: Path

    def load_input(self) -> TextIO:
        asset = self.input_folder / f"day{self.day}.txt"
        return asset.open()

    @abstractmethod
    def parse_input(self, input: TextIO):
        pass

    def run(self, variant):
        with self.load_input() as input:
            input = self.parse_input(input)
        method = getattr(self, f"run_{variant}")
        return method(input)


@dataclass
class SameComputationAdventDay(BaseAdventDay, metaclass=ABCMeta):
    @abstractmethod
    def compute(self, var, input):
        pass

    def run(self, variant):
        with self.load_input() as input:
            input = self.parse_input(input)
        return self.compute(variant, input)
