import itertools as it
from dataclasses import dataclass
from functools import cache, reduce
from typing import TextIO, override

from advent.common import BaseAdventDay

cached_ord = cache(ord)


@dataclass
class Day3(BaseAdventDay[list[str]]):
    def get_score(self, letter: str) -> int:
        o = ord(letter)
        if cached_ord("a") <= o <= cached_ord("z"):
            return o - cached_ord("a") + 1
        elif cached_ord("A") <= o <= cached_ord("Z"):
            return o - cached_ord("A") + 27
        else:
            raise ValueError(f"Invalid letter {letter}")

    @override
    def parse_input(self, input: TextIO) -> list[str]:
        return [row.strip() for row in input]

    @override
    def _run_1(self, input: list[str]) -> int:
        def process_row(row: str):
            half = len(row) // 2
            left, right = row[:half], row[half:]
            return frozenset(left) & frozenset(right)

        return sum(max(self.get_score(c) for c in process_row(r)) for r in input)

    @override
    def _run_2(self, input: list[str]) -> int:
        tot = 0
        for group in it.batched(input, 3):
            ret = reduce(set[str].__and__, map(set, group))
            assert ret
            badge = ret.pop()
            tot += self.get_score(badge)
        return tot
