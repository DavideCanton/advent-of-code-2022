from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, TextIO, override


class ResultProtocol(Protocol):
    def __str__(self) -> str: ...


type Variant = Literal[1, 2]


@dataclass
class BaseAdventDay[T](metaclass=ABCMeta):
    input_file: Path

    def load_input(self) -> TextIO:
        return self.input_file.open()

    @abstractmethod
    def parse_input(self, input: TextIO) -> T:
        pass

    @abstractmethod
    def _run_1(self, input: T) -> ResultProtocol:
        pass

    @abstractmethod
    def _run_2(self, input: T) -> ResultProtocol:
        pass

    def run(self, variant: Variant) -> ResultProtocol:
        with self.load_input() as input:
            input = self.parse_input(input)

        match variant:
            case 1:
                return self._run_1(input)
            case 2:
                return self._run_2(input)


@dataclass
class SameComputationAdventDay[T](BaseAdventDay[T], metaclass=ABCMeta):
    @abstractmethod
    def compute(self, var: Variant, input: T) -> ResultProtocol:
        pass

    @override
    def _run_1(self, input: T) -> ResultProtocol:
        return self._common_run(1, input)

    @override
    def _run_2(self, input: T) -> ResultProtocol:
        return self._common_run(2, input)

    def _common_run(self, variant: Variant, input: T) -> ResultProtocol:
        return self.compute(variant, input)
