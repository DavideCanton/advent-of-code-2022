from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, TextIO, override

from advent.common import SameComputationAdventDay, Variant

type Move = Literal["U", "D", "L", "R"]
type Pos = tuple[int, int]
Moves = list[tuple[Move, int]]


def components(p: Pos) -> Iterable[Pos]:
    x, y = p
    if x == 0 and y == 0:
        raise ValueError("Invalid")

    if x != 0:
        yield (x, 0)
    if y != 0:
        yield (0, y)


@dataclass
class Day9(SameComputationAdventDay[Moves]):
    @override
    def parse_input(self, input: TextIO) -> Moves:
        moves: list[tuple[Move, int]] = []
        for line in input:
            line = line.strip().split()
            assert len(line) == 2
            move: Move = line[0]  # type: ignore
            moves.append((move, int(line[1])))

        return moves

    @override
    def compute(self, var: Variant, input: Moves):
        body_size = 2 if var == 1 else 10

        positions: list[Pos] = [(0, 0)] * body_size
        visited: set[Pos] = set()

        for move in input:
            for _ in range(move[1]):
                positions[0] = self._move(positions[0], move[0])
                for i in range(1, len(positions)):
                    positions[i] = self._fix(positions[i - 1], positions[i])
                visited.add(positions[-1])

        return len(visited)

    def _move(self, pos: Pos, move: Move) -> Pos:
        x, y = pos
        match move:
            case "L":
                return (x - 1, y)
            case "R":
                return (x + 1, y)
            case "U":
                return (x, y - 1)
            case "D":
                return (x, y + 1)

    def _fix(self, cur: Pos, next: Pos) -> Pos:
        dist = (next[0] - cur[0], next[1] - cur[1])

        if max(map(abs, dist)) <= 1:  # type: ignore
            return next

        moves: list[Move] = []

        for c in components(dist):
            match c:
                case (x, 0) if x > 0:
                    moves.append("L")
                case (x, 0) if x < 0:
                    moves.append("R")
                case (0, y) if y > 0:
                    moves.append("U")
                case (0, y) if y < 0:
                    moves.append("D")
                case _:
                    pass

        for m in moves:
            next = self._move(next, m)

        return next
