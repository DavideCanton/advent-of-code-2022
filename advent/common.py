from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TextIO, TypeVar

_I = TypeVar("_I")


@dataclass
class BaseAdventDay(Generic[_I], metaclass=ABCMeta):
    input_file: Path

    def load_input(self) -> TextIO:
        return self.input_file.open()

    @abstractmethod
    def parse_input(self, input: TextIO) -> _I:
        pass

    @abstractmethod
    def _run_1(self, input: _I):
        pass

    @abstractmethod
    def _run_2(self, input: _I):
        pass

    def run(self, variant: int) -> Any:
        with self.load_input() as input:
            input = self.parse_input(input)

        match variant:
            case 1:
                return self._run_1(input)
            case 2:
                return self._run_2(input)
            # should never happen, validated by the parser
            case _ as v:
                raise ValueError(f"Unsupported variant: {v}")


@dataclass
class SameComputationAdventDay(BaseAdventDay[_I], metaclass=ABCMeta):
    @abstractmethod
    def compute(self, var: int, input: _I):
        pass

    def _run_1(self, input: _I):
        return self._common_run(1, input)

    def _run_2(self, input: _I):
        return self._common_run(2, input)

    def _common_run(self, variant: int, input: _I):
        return self.compute(variant, input)
