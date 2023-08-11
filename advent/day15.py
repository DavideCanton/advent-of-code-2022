from __future__ import annotations

import re
from bisect import bisect_left
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from functools import cached_property
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


@dataclass
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

        for s in input:
            for p in _border(s, 0, target):
                if all(
                    _manhattan(s2.sensor, p) > s2.distance for s2 in input if s != s2
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


def _border(s: Sensor, min_v: int, max_v: int) -> Iterator[Pos]:
    sx, sy = s.sensor

    if sx < min_v or sx > max_v:
        return

    d = s.distance
    min_dd = max(min_v - sy, -d - 1)
    max_dd = min(max_v - sy, d + 1)

    for dd in range(min_dd, max_dd + 1):
        h = d + 1 - abs(dd)
        y = sy + dd
        yield (sx + h, y)
        if h != 0:
            yield (sx - h, y)
