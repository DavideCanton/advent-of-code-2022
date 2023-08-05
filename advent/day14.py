from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import islice
from typing import TextIO

from advent.common import BaseAdventDay

Pos = tuple[int, int]


@dataclass(frozen=True)
class Path:
    pos: tuple[Pos, ...]

    def __iter__(self):
        return iter(self.pos)

    def pairwise(self) -> Iterator[tuple[Pos, Pos]]:
        it1 = iter(self.pos)
        it2 = islice(self.pos, 1, None)
        for p1, p2 in zip(it1, it2):
            yield p1, p2

    @lru_cache(1024)  # noqa: B019
    def __contains__(self, pos: Pos) -> bool:
        x, y = pos
        for p1, p2 in self.pairwise():
            x1, y1 = p1
            x2, y2 = p2

            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            if x1 <= x <= x2 and y1 <= y <= y2:
                return True

        return False


@dataclass
class Board:
    paths: list[Path]
    start: Pos = field(default=(500, 0))
    sand: set[Pos] = field(init=False, default_factory=set)
    edge: int = field(init=False)
    using: bool = field(init=False, default=False)

    def __post_init__(self):
        self.edge = max(y for p in self.paths for (_, y) in p)

    @contextmanager
    def use(self):
        try:
            self.using = True
            yield
        finally:
            self.using = False
            for p in self.paths:
                p.__contains__.cache_clear()

    def simulate(self, verbose=False, overwrite=False, sleep=None):
        if not self.using:
            raise ValueError("invalid state")
        self.sand.clear()
        abyss_reached = False

        if verbose:
            ctx = open("out.txt", "w")
        else:
            ctx = nullcontext(TextIO())

        with ctx as fo:
            if verbose:
                self.print_board(fo, overwrite)

            while not abyss_reached:
                cur = self.start
                while True:
                    if sleep is not None:
                        time.sleep(sleep)

                    if verbose:
                        self.print_board(fo, overwrite, cur)

                    next_pos = self._next_pos(cur)
                    if not next_pos:
                        break
                    if next_pos[1] > self.edge:
                        abyss_reached = True
                        break
                    cur = next_pos

                if not abyss_reached:
                    self.sand.add(cur)
                    if verbose:
                        self.print_board(fo, overwrite)

            return len(self.sand)

    def print_board(self, fo: TextIO, overwrite, cur: Pos | None = None):
        if overwrite:
            fo.seek(0)
        print(self.as_str(cur), file=fo)
        print("=" * 100, file=fo)
        fo.flush()

    def as_str(self, cur: Pos | None = None) -> str:
        left = min(x for p in self.paths for (x, _) in p)
        right = max(x for p in self.paths for (x, _) in p)

        buf = [["."] * (right - left + 1) for _ in range(self.edge + 1)]

        for x, y in self.sand:
            buf[y][x - left] = "o"

        if cur:
            x, y = cur
            buf[y][x - left] = "x"

        for p in self.paths:
            for p1, p2 in p.pairwise():
                if p1[0] == p2[0]:
                    from_ = min(p1[1], p2[1])
                    to = max(p1[1], p2[1])
                    for y in range(from_, to + 1):
                        buf[y][p1[0] - left] = "#"
                else:
                    from_ = min(p1[0], p2[0])
                    to = max(p1[0], p2[0])
                    for x in range(from_, to + 1):
                        buf[p1[1]][x - left] = "#"

        return "\n".join("".join(row) for row in buf)

    def _next_pos(self, cur: Pos) -> Pos | None:
        x, y = cur
        ny = y + 1
        for nx in [x, x - 1, x + 1]:
            new = (nx, ny)
            if new not in self.sand and not any(new in p for p in self.paths):
                return new
        return None


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
            output.append(Path(tuple(pos)))

        return Board(output)

    def _run_1(self, input: Board):
        with input.use():
            return input.simulate(verbose=False, overwrite=False) # 805

    def _run_2(self, input: Board):
        return None

