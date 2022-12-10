import re

from advent.common import SameComputationAdventDay

REGEX = re.compile(r"^(\d+)-(\d+),(\d+)-(\d+)$")


class Day4(SameComputationAdventDay):
    def get_input(self, variant) -> tuple:
        def process(row):
            try:
                d1, d2, d3, d4 = map(int, REGEX.match(row).groups())
                return (d1, d2), (d3, d4)
            except AttributeError:
                raise ValueError(f"Invalid row: {row}")

        input = self.load_asset("input.txt")
        return ([process(row.strip()) for row in input],)

    def compute(self, var, rows):
        if var == 1:
            fn = self._contained
        else:
            fn = self._overlaps

        return sum(1 if fn(*p1, *p2) else 0 for (p1, p2) in rows)

    def _contained(self, a, b, c, d):
        return (a <= c and b >= d) or (a >= c and b <= d)

    def _overlaps(self, a, b, c, d):
        return b >= c and a <= d


Instance = Day4()
