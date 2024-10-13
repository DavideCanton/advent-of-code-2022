from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto
from itertools import pairwise
from typing import override

from advent.common import BaseAdventDay

Pos = tuple[int, int]


class CellType(Enum):
    Empty = auto()
    Wall = auto()
    Sand = auto()


class Path:
    all_pos: frozenset[Pos]

    def __init__(self, pos: Iterable[Pos]) -> None:
        all_pos: set[Pos] = set()

        for p1, p2 in pairwise(pos):
            if p1[0] == p2[0]:
                from_ = min(p1[1], p2[1])
                to = max(p1[1], p2[1])
                for y in range(from_, to + 1):
                    all_pos.add((p1[0], y))
            else:
                from_ = min(p1[0], p2[0])
                to = max(p1[0], p2[0])
                for x in range(from_, to + 1):
                    all_pos.add((x, p1[1]))

        self.all_pos = frozenset(all_pos)

    def __iter__(self):
        return iter(self.all_pos)

    def __contains__(self, pos: Pos) -> bool:
        return pos in self.all_pos


class Board:
    paths: list[Path]
    blocked: dict[Pos, CellType]

    def __init__(self, paths: list[Path], start: Pos = (500, 0)):
        self.paths = paths
        self.start = start
        self.sand = 0
        self.blocked = {}
        self.edge = max(y for p in self.paths for (_, y) in p)

    def simulate(self, add_bottom_at: int | None = None):
        end = False

        if add_bottom_at is not None:
            edge = self.edge = self.edge + add_bottom_at
            x_start = self.start[0]
            bottom = Path([(x_start - edge, edge), (x_start + edge, edge)])
            self.paths.append(bottom)
            self.edge += add_bottom_at

        while not end:
            cur = self.start
            while True:
                next_pos = self._next_pos(cur)
                if not next_pos:
                    break
                if next_pos[1] > self.edge:
                    end = True
                    break
                cur = next_pos

            if not end:
                self.sand += 1
                self.blocked[cur] = CellType.Sand

            if cur == self.start:
                end = True

        return self.sand

    def _next_pos(self, cur: Pos) -> Pos | None:
        x, y = cur
        ny = y + 1
        for nx in [x, x - 1, x + 1]:
            new = (nx, ny)
            if not self._is_blocked(new):
                return new
        return None

    def _is_blocked(self, pos: Pos) -> bool:
        cell = self.blocked.get(pos)
        if cell is None:
            if wall_present := any(pos in p for p in self.paths):
                self.blocked[pos] = CellType.Wall
            else:
                self.blocked[pos] = CellType.Empty
            return wall_present
        return cell != CellType.Empty


@dataclass
class Day14(BaseAdventDay[Board]):
    @override
    def parse_input(self) -> Board:
        output: list[Path] = []
        for line in self.input:
            parts = line.split("->")
            pos: list[Pos] = []
            for p in parts:
                p = p.strip().split(",")
                assert len(p) == 2
                pos.append(tuple(map(int, p)))  # type: ignore
            output.append(Path(tuple(pos)))

        return Board(output)

    @override
    def _run_1(self, input: Board):
        return input.simulate()

    @override
    def _run_2(self, input: Board):
        return input.simulate(2)
