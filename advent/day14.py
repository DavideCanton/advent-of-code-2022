from __future__ import annotations

from dataclasses import dataclass, field
from typing import TextIO

from advent.common import BaseAdventDay

Pos = tuple[int, int]


@dataclass
class Path:
    pos: list[Pos]

    def __contains__(self, pos: Pos) -> bool:
        it1 = iter(self.pos)
        it2 = iter(self.pos)
        next(it2)
        x, y = pos

        for (x1, y1), (x2, y2) in zip(it1, it2):
            if x1 <= x <= x2 and y1 <= y <= y2:
                return True

        return False


@dataclass
class Board:
    paths: list[Path]
    sand: set[Pos] = field(init=False, default_factory=set)


@dataclass
class Day14(BaseAdventDay[Board]):
    day = 14

    def parse_input(self, input: TextIO) -> Board:
        output = []
        for line in input:
            parts = line.split("->")
            pos = []
            for p in parts:
                p = p.strip().split(",")
                assert len(p) == 2
                pos.append(tuple(map(int, p)))
            output.append(Path(pos))

        return Board(output)

    def _run_1(self, input: Board):
        return None

    def _run_2(self, input: Board):
        return None
