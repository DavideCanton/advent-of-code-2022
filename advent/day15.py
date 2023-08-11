from __future__ import annotations

import re
from bisect import bisect_left
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, lru_cache
from itertools import combinations
from typing import ClassVar, TextIO

from advent.common import BaseAdventDay

Pos = tuple[int, int]


@dataclass(order=True, repr=False)
class Range:
    from_: int
    to: int

    def can_merge_with(self, other: Range) -> bool:
        return self.to - other.from_ >= -1

    def merge_with(self, other: Range) -> Range:
        return Range(min(self.from_, other.from_), max(self.to, other.to))

    @property
    def cells_inside(self) -> int:
        return self.to - self.from_ + 1

    def __repr__(self) -> str:
        return f"<{self.from_}, {self.to}>"


@dataclass(unsafe_hash=True)
class Sensor:
    sensor: Pos
    beacon: Pos

    REGEX: ClassVar[re.Pattern] = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )

    @cached_property
    def distance(self) -> int:
        return _manhattan(self.beacon, self.sensor)

    @classmethod
    def parse(cls, row: str) -> Sensor:
        if match := cls.REGEX.match(row):
            sx, sy, bx, by = map(int, match.groups())
            return cls((sx, sy), (bx, by))
        raise ValueError(row)


@dataclass
class Day15(BaseAdventDay[list[Sensor]]):
    day = 15

    def parse_input(self, input: TextIO) -> list[Sensor]:
        return [Sensor.parse(row) for row in input]

    def _run_1(self, input: list[Sensor]) -> int:
        target = 2000000
        covered, beacons = self._covered_row(input, target)
        return sum(r.cells_inside for r in covered) - len(beacons)

    def _run_2(self, input: list[Sensor]):
        target = 4000000
        freq = 4000000

        for s1, s2 in combinations(input, 2):
            for (x1, y1), (x2, y2) in _border_bounds(s1):
                for (x3, y3), (x4, y4) in _border_bounds(s2):
                    d = _det(x2 - x1, x3 - x4, y2 - y1, y3 - y4)
                    if d == 0:
                        # parallel borders, skip
                        continue
                    s = _det(x3 - x1, x3 - x4, y3 - y1, y3 - y4) / d
                    t = _det(x2 - x1, x3 - x1, y2 - y1, y3 - y1) / d

                    if 0 <= s <= 1 and 0 <= t <= 1:
                        p = (int(x1 + s * (x2 - x1)), int(y1 + s * (y2 - y1)))
                        if (
                            0 <= p[0] <= target
                            and 0 <= p[1] <= target
                            and all(
                                p != s.beacon and _manhattan(s.sensor, p) > s.distance
                                for s in input
                            )
                        ):
                            return p[0] * freq + p[1]

    def _covered_row(
        self,
        input: list[Sensor],
        target: int,
        from_: int | None = None,
        to: int | None = None,
    ) -> tuple[list[Range], set[int]]:
        covered: list[Range] = []
        beacons = set()

        get_from = _getter(from_, max)
        get_to = _getter(to, min)

        for s in input:
            sx, sy = s.sensor
            d = s.distance

            if target >= sy:
                r = sy + d - target
            else:
                r = target - sy + d

            if r < 0:
                continue

            if s.beacon[1] == target:
                beacons.add(s.beacon[0])

            rg = Range(get_from(sx - r), get_to(sx + r))
            t = bisect_left(covered, rg)

            p = t - 1
            while p >= 0:
                cp = covered[p]
                if not cp.can_merge_with(rg):
                    break
                rg = cp.merge_with(rg)
                p -= 1

            n = t
            while n < len(covered):
                cn = covered[n]
                if not rg.can_merge_with(cn):
                    break
                rg = rg.merge_with(cn)
                n += 1

            covered[p + 1 : n] = [rg]

        return covered, beacons


def _getter(val: int | None, fn: Callable[[int, int], int]) -> Callable[[int], int]:
    if val is None:
        return lambda x: x
    else:
        return lambda x: fn(x, val)


def _manhattan(p1: Pos, p2: Pos) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@lru_cache(30)
def _border_bounds(s: Sensor) -> tuple[tuple[Pos, Pos], ...]:
    dist = s.distance + 1
    sx, sy = s.sensor

    u = (sx, sy - dist)
    d = (sx, sy + dist)
    l = (sx - dist, sy)  # noqa: E741
    r = (sx + dist, sy)

    return ((u, l), (u, r), (d, l), (d, r))


def _det(a, b, c, d):
    return a * d - b * c
