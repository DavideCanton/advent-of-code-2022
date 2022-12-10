import re
from dataclasses import dataclass

from advent.common import SameComputationAdventDay

REGEX = re.compile(r"^(\d+)-(\d+),(\d+)-(\d+)$")
R = tuple[int, int]


@dataclass
class Day4(SameComputationAdventDay):
    day = 4

    def get_input(self) -> list[tuple[R, R]]:
        def process(row: str):
            try:
                d1, d2, d3, d4 = map(int, REGEX.match(row).groups())
                return (d1, d2), (d3, d4)
            except AttributeError:
                raise ValueError(f"Invalid row: {row}")

        input = self.load_input()
        return [process(row.strip()) for row in input]

    def compute(self, var: int, rows: list[tuple[R, R]]) -> int:
        if var == 1:
            fn = self._contained
        else:
            fn = self._overlaps

        return sum(1 if fn(*p1, *p2) else 0 for (p1, p2) in rows)

    def _contained(self, a: int, b: int, c: int, d: int) -> bool:
        return (a <= c and b >= d) or (a >= c and b <= d)

    def _overlaps(self, a: int, b: int, c: int, d: int) -> bool:
        return b >= c and a <= d


ProblemClass = Day4
