from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Literal

from advent.common import SameComputationAdventDay

Play = Literal["P", "R", "S"]
OppChar = Literal["A", "B", "C"]
YourChar = Literal["X", "Y", "Z"]

P: list[Play] = list("RPS")
OPPONENT: dict[OppChar, Play] = dict(zip("ABC", P))
SCORES: dict[Play, int] = dict(zip(P, range(1, 4)))

WINS: dict[Play, Play] = {"S": "P", "R": "S", "P": "R"}
LOSES: dict[Play, Play] = {v: k for k, v in WINS.items()}


class Base(metaclass=ABCMeta):
    @abstractmethod
    def _compute_iy(self, io: Play, yours: YourChar) -> Play:
        pass

    def _compute_score(self, io: Play, iy: Play) -> int:
        if io == iy:
            return 3
        elif WINS[io] == iy:
            return 0
        else:
            return 6

    def __call__(self, opp: OppChar, yours: YourChar) -> int:
        io = OPPONENT[opp]
        iy = self._compute_iy(io, yours)
        return SCORES[iy] + self._compute_score(io, iy)


class Result1(Base):
    def __init__(self):
        self.yours_table: dict[YourChar, Play] = dict(zip("XYZ", P))

    def _compute_iy(self, io: Play, yours: YourChar) -> Play:
        return self.yours_table[yours]


class Result2(Base):
    def _compute_iy(self, io: Play, yours: YourChar) -> Play:
        match yours:
            case "Y":
                return io
            case "X":
                return WINS[io]
            case "Z":
                return LOSES[io]


@dataclass
class Day2(SameComputationAdventDay):
    day = 2

    def get_input(self) -> Iterable[list[str]]:
        return (r.strip().split() for r in self.load_input())

    def compute(self, variant: int, rows: Iterable[list[str]]) -> int:
        if variant == 1:
            fn = Result1()
        else:
            fn = Result2()

        return sum(fn(*r) for r in rows)


ProblemClass = Day2
