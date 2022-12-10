import itertools as it
from functools import cache, reduce

from advent.common import BaseAdventDay, load_asset

cached_ord = cache(ord)


class Day3(BaseAdventDay):
    def get_score(self, letter):
        o = ord(letter)
        if cached_ord("a") <= o <= cached_ord("z"):
            return o - cached_ord("a") + 1
        elif cached_ord("A") <= o <= cached_ord("Z"):
            return o - cached_ord("A") + 27
        else:
            raise ValueError(f"Invalid letter {letter}")

    def get_input(self, variant) -> tuple:
        return ([row.strip() for row in load_asset(__file__, "input.txt")],)

    def run_1(self, rows):
        def process_row(row):
            half = len(row) // 2
            left, right = row[:half], row[half:]
            return frozenset(left) & frozenset(right)

        return sum(max(self.get_score(c) for c in process_row(r)) for r in rows)

    def run_2(self, rows):
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


Instance = Day3()
