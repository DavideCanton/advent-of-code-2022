import itertools as it
import re
from dataclasses import dataclass
from typing import TextIO, override

from advent.common import SameComputationAdventDay, Variant


@dataclass
class Move:
    target: int
    from_: str
    to: str


State = dict[str, list[str]]


@dataclass
class Input:
    crates: State
    moves: list[Move]


@dataclass
class Day5(SameComputationAdventDay[Input]):
    @override
    def parse_input(self) -> Input:
        crates = self._load_crates(self.input)
        moves = self._load_moves(self.input)

        return Input(crates, moves)

    @override
    def compute(self, var: Variant, input: Input):
        if var == 1:
            apply_fn = self._apply_1
        else:
            apply_fn = self._apply_2

        state = input.crates

        for m in input.moves:
            apply_fn(m, state)

        return "".join([r[-1] for r in state.values()])

    def _apply_1(self, move: Move, state: State):
        for _ in range(move.target):
            state[move.to].append(state[move.from_].pop())

    def _apply_2(self, move: Move, state: State):
        state[move.to].extend(state[move.from_][-move.target :])
        state[move.from_] = state[move.from_][: -move.target]

    def _load_crates(self, input: TextIO) -> State:
        buffer: list[str] = []

        for row in input:
            row = row.strip("\n")
            if not row:
                break
            buffer.append(row)

        keys = buffer.pop().split()
        crates: dict[str, list[str]] = {k: [] for k in keys}

        while buffer:
            row = buffer.pop()
            for i, part in enumerate(it.batched(row, 4)):
                if part[0] == "[":
                    crates[keys[i]].append(part[1])

        return crates

    def _load_moves(self, input: TextIO) -> list[Move]:
        regex = re.compile(r"^move (\d+) from (\w+) to (\w+)$")
        moves: list[Move] = []
        for row in input:
            match = regex.match(row.strip())
            assert match
            target, from_, to = match.groups()
            moves.append(Move(int(target), from_, to))
        return moves
