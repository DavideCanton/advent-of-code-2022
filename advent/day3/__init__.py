import itertools as it
from dataclasses import dataclass
from functools import cache, reduce
from typing import TextIO

from advent.common import BaseAdventDay

cached_ord = cache(ord)


@dataclass
class Day3(BaseAdventDay):
    day = 3

    def get_score(self, letter) -> int:
        o = ord(letter)
        if cached_ord("a") <= o <= cached_ord("z"):
            return o - cached_ord("a") + 1
        elif cached_ord("A") <= o <= cached_ord("Z"):
            return o - cached_ord("A") + 27
        else:
            raise ValueError(f"Invalid letter {letter}")

    def parse_input(self, input: TextIO) -> list[str]:
        return [row.strip() for row in input]

    def run_1(self, rows: list[str]) -> int:
        def process_row(row):
            half = len(row) // 2
            left, right = row[:half], row[half:]
            return frozenset(left) & frozenset(right)

        return sum(max(self.get_score(c) for c in process_row(r)) for r in rows)

    def run_2(self, rows: list[str]) -> int:
        tot = 0
        for i in it.count():
            start = 3 * i
            if start >= len(rows):
                break
            group = rows[start : start + 3]
            ret = reduce(frozenset.__and__, map(frozenset, group))
            assert ret
            badge = next(iter(ret))
            tot += self.get_score(badge)
        return tot


ProblemClass = Day3
