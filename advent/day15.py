from __future__ import annotations

import re
from bisect import bisect_left
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from functools import cached_property
from itertools import pairwise
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
        sx, sy = self.sensor
        bx, by = self.beacon
        return abs(sx - bx) + abs(sy - by)

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
        covered, beacons = self._search(input, target)
        return sum(r.cells_inside for r in covered) - len(beacons)

    def _run_2(self, input: list[Sensor]):
        target = 4000000
        freq = 4000000

        cnt1 = range(target // 2 + 1)
        cnt2 = range(target, target // 2, -1)

        for y in _alternate(cnt1, cnt2):
            covered, beacons = self._search(input, y, 0, target)

            xs = set()

            if covered and covered[0].from_ > 0:
                xs.update(range(covered[0].from_))
            elif covered and covered[-1].to < target:
                xs.update(range(covered[1].to, target + 1))

            for r1, r2 in pairwise(covered):
                xs.update(range(r1.to + 1, r2.from_))

            for b in beacons:
                try:
                    xs.remove(b)
                except KeyError:
                    pass

            assert len(xs) <= 1
            if len(xs) == 1:
                x = xs.pop()
                return x * freq + y

    def _search(
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


def _alternate(i1: Iterable[int], i2: Iterable[int]) -> Iterator[int]:
    i1 = iter(i1)
    i2 = iter(i2)
    for a, b in zip(i1, i2):
        yield a
        yield b

    yield from i1
    yield from i2
