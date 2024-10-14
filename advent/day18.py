from __future__ import annotations

from collections import deque
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
        cubes = set(input)
        mx = max(c.x for c in input) + 1
        my = max(c.y for c in input) + 1
        mz = max(c.z for c in input) + 1

        start = Cube(-1, -1, -1)

        frontier = deque([start])
        visited = set[Cube]()
        sides = 0

        while frontier:
            c = frontier.popleft()
            if c in visited or (c.x > mx or c.y > my or c.z > mz):
                continue

            visited.add(c)

            adjs = set(c.adjacents())
            for adj in adjs:
                if adj in cubes:
                    sides += 1

                if (
                    adj not in cubes
                    and adj not in visited
                    and all(q >= -1 for q in (adj.x, adj.y, adj.z))
                ):
                    frontier.append(adj)

        return sides
