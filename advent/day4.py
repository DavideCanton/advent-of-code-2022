import re
from dataclasses import dataclass
from typing import override

from advent.common import SameComputationAdventDay, Variant

REGEX = re.compile(r"^(\d+)-(\d+),(\d+)-(\d+)$")
R = tuple[int, int]


@dataclass
class Day4(SameComputationAdventDay[list[tuple[R, R]]]):
    @override
    def parse_input(self) -> list[tuple[R, R]]:
        def process(row: str):
            try:
                match = REGEX.match(row)
                assert match
                d1, d2, d3, d4 = map(int, match.groups())
                return (d1, d2), (d3, d4)
            except AttributeError:
                raise ValueError(f"Invalid row: {row}") from None

        return [process(row.strip()) for row in self.input]

    @override
    def compute(self, var: Variant, input: list[tuple[R, R]]) -> int:
        if var == 1:
            fn = self._contained
        else:
            fn = self._overlaps

        return sum(1 if fn(*p1, *p2) else 0 for (p1, p2) in input)

    def _contained(self, a: int, b: int, c: int, d: int) -> bool:
        return (a <= c and b >= d) or (a >= c and b <= d)

    def _overlaps(self, a: int, b: int, c: int, d: int) -> bool:
        return b >= c and a <= d
