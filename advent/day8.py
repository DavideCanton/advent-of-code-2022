from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter, mul
from typing import TextIO, override

from advent.common import BaseAdventDay

type Matrix = list[list[int]]
Grid = tuple[Matrix, Matrix]


@dataclass
class Day8(BaseAdventDay[Grid]):
    @override
    def parse_input(self, input: TextIO) -> Grid:
        by_row = [list(map(int, line.strip())) for line in input]
        by_col = list(map(list, zip(*by_row)))
        return by_row, by_col

    @override
    def _run_1(self, input: Grid) -> int:
        r = len(input[0])
        c = len(input[1])
        edges = 2 * r + 2 * (c - 2)
        return (
            sum(
                int(any(x is None for (_, x) in self._blocked(input, i, j)))
                for i in range(1, r - 1)
                for j in range(1, c - 1)
            )
            + edges
        )

    @override
    def _run_2(self, input: Grid) -> int:
        r = len(input[0])
        c = len(input[1])
        return max(
            self._score(input, i, j) for i in range(1, r - 1) for j in range(1, c - 1)
        )

    def _score(self, grid: Grid, i: int, j: int) -> int:
        bl = self._blocked(grid, i, j)
        return reduce(mul, map(itemgetter(0), bl))

    def _blocked(self, grid: Grid, i: int, j: int) -> Iterable[tuple[int, int | None]]:
        row = grid[0][i]
        col = grid[1][j]
        val = row[j]
        return (
            next(((i, v) for i, v in enumerate(x, start=1) if v >= val), (len(x), None))
            for x in (row[j - 1 :: -1], row[j + 1 :], col[i - 1 :: -1], col[i + 1 :])
        )
