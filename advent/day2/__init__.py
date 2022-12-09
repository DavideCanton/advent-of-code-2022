from abc import ABCMeta, abstractmethod

from common import SameComputationAdventDay, load_asset

P = "RPS"
OPPONENT = dict(zip("ABC", P))
SCORES = dict(zip(P, range(1, 4)))

WINS = {"S": "P", "R": "S", "P": "R"}
LOSES = {v: k for k, v in WINS.items()}


class Base(metaclass=ABCMeta):
    @abstractmethod
    def _compute_iy(io, yours):
        pass

    def _compute_score(self, io, iy):
        if io == iy:
            return 3
        elif WINS[io] == iy:
            return 0
        else:
            return 6

    def __call__(self, opp, yours):
        io = OPPONENT[opp]
        iy = self._compute_iy(io, yours)
        return SCORES[iy] + self._compute_score(io, iy)


class Result1(Base):
    def __init__(self):
        self.yours_table = dict(zip("XYZ", P))

    def _compute_iy(self, io, yours):
        return self.yours_table[yours]


class Result2(Base):
    def _compute_iy(self, io, yours):
        match yours:
            case "Y":
                return io
            case "X":
                return WINS[io]
            case "Z":
                return LOSES[io]


class Day2(SameComputationAdventDay):
    def get_input(self, variant) -> tuple:
        return (load_asset(__file__, "strategy.txt"),)

    def compute(self, variant, rows):
        if variant == 1:
            fn = Result1()
        else:
            fn = Result2()

        return sum(fn(*r.strip().split()) for r in rows)


Instance = Day2()
