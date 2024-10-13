from __future__ import annotations

from dataclasses import dataclass
from typing import override

from advent.common import BaseAdventDay


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def adjacents(self) -> set[Cube]:
        return {
            Cube(self.x + x, self.y + y, self.z + z)
            for x, y, z in (
                (1, 0, 0),
                (-1, 0, 0),
                (0, 1, 0),
                (0, -1, 0),
                (0, 0, 1),
                (0, 0, -1),
            )
        }


@dataclass
class Day18(BaseAdventDay[list[Cube]]):
    @override
    def parse_input(self) -> list[Cube]:
        return [Cube(*map(int, line.strip().split(","))) for line in self.input]

    @override
    def _run_1(self, input: list[Cube]):
        cubes = set(input)
        sides = 0

        for cube in cubes:
            adjacents = sum(1 for adj in cube.adjacents() if adj in cubes)
            assert adjacents <= 6
            sides += 6 - adjacents

        return sides

    @override
    def _run_2(self, input: list[Cube]):
        pass
