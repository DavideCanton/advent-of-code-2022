from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, TextIO, override

from advent.common import BaseAdventDay

_REG: dict[str, type[Instr]] = {}


@dataclass
class Instr(metaclass=ABCMeta):
    CYCLES: ClassVar[int]
    NAME: ClassVar[str]

    def __init_subclass__(cls) -> None:
        _REG[cls.NAME] = cls

    @staticmethod
    def parse(line: str) -> Instr:
        name, *args = line.strip().split()
        cls = _REG[name]
        return cls._parse(*args)

    @classmethod
    @abstractmethod
    def _parse(cls, *args: Any) -> Instr:
        pass

    @abstractmethod
    def apply(self, x: int) -> int:
        pass


@dataclass
class AddX(Instr):
    CYCLES = 2
    NAME = "addx"
    amount: int

    @classmethod
    @override
    def _parse(  # pyright: ignore[reportIncompatibleMethodOverride]
        cls, amount: int
    ) -> AddX:
        return AddX(int(amount))

    @override
    def apply(self, x: int) -> int:
        return x + self.amount


@dataclass
class NoOp(Instr):
    CYCLES = 1
    NAME = "noop"

    @classmethod
    @override
    def _parse(cls, *args: Any) -> NoOp:
        return NoOp()

    @override
    def apply(self, x: int) -> int:
        return x


@dataclass
class Day10(BaseAdventDay[list[Instr]]):
    @override
    def parse_input(self, input: TextIO) -> list[Instr]:
        return [Instr.parse(line) for line in input]

    @override
    def _run_1(self, input: list[Instr]) -> int:
        x = 1
        cycles = 1
        strength = 0
        target = 20

        for instr in input:
            instr_cycles = instr.CYCLES
            cycles += instr_cycles
            new_x = instr.apply(x)

            if cycles >= target:
                if cycles > target:
                    x_to_add = x
                else:
                    x_to_add = new_x

                strength += x_to_add * target
                target += 40

            x = new_x

        return strength

    @override
    def _run_2(self, input: list[Instr]) -> str:
        x = 1
        cycles = 0
        line = 40
        buf: list[list[str]] = []

        for instr in input:
            for c in range(cycles, cycles + instr.CYCLES):
                pixel = c % line
                if pixel == 0:
                    buf.append([])

                if x - 1 <= pixel <= x + 1:
                    buf[-1].append("#")
                else:
                    buf[-1].append(".")

            x = instr.apply(x)
            cycles += instr.CYCLES

        return "\n".join("".join(x) for x in buf)
