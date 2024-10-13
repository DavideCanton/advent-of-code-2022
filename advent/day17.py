from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cached_property
from itertools import count, cycle
from typing import Self, override

from advent.common import BaseAdventDay

PRINT = False


class Direction(Enum):
    Left = auto()
    Right = auto()


@dataclass(frozen=True)
class Jet:
    index: int
    direction: Direction


@dataclass(frozen=True)
class Piece:
    index: int
    board: Board

    @cached_property
    def shape(self) -> tuple[int, int]:
        return self.board.shape


@dataclass
class Board:
    cols: int
    board: list[list[bool]] = field(init=False, default_factory=list)

    @classmethod
    def from_(cls, board: list[list[bool]]) -> Self:
        b = cls(len(board[0]))
        b.board = board
        return b

    @cached_property
    def shape(self) -> tuple[int, int]:
        return len(self.board[0]), len(self.board)

    def __getitem__(self, item: tuple[int, int]) -> bool:
        xr, yr = item
        return self.board[yr][xr]

    def __setitem__(self, key: tuple[int, int], value: bool) -> None:
        x, y = key
        self.board[y][x] = value

    def __len__(self) -> int:
        return len(self.board)

    def append_row_top(self, n: int = 1) -> None:
        for _ in range(n):
            self.board.append([False] * self.cols)

    def ensure_rows(self, n: int) -> None:
        to_add = n - len(self.board)
        if to_add > 0:
            self.append_row_top(to_add)

    def can_move_left(self, rock: Piece, x: int, y: int) -> bool:
        if x == 0:
            return False

        for xr in range(rock.shape[0]):
            for yr in range(rock.shape[1]):
                if rock.board[xr, yr] and self[x - 1 + xr, yr + y]:
                    return False

        return True

    def can_move_right(self, rock: Piece, x: int, y: int) -> bool:
        if x == self.cols - rock.shape[0]:
            return False

        for xr in range(rock.shape[0]):
            for yr in range(rock.shape[1]):
                if rock.board[xr, yr] and self[x + 1 + xr, yr + y]:
                    return False

        return True

    def can_move_down(self, rock: Piece, x: int, y: int) -> bool:
        if y == 0:
            return False

        for xr in range(rock.shape[0]):
            for yr in range(rock.shape[1]):
                if rock.board[xr, yr] and self[x + xr, yr - 1 + y]:
                    return False

        return True

    def apply(self, board: Board, x: int, y: int) -> None:
        xs, ys = board.shape
        for xr in range(xs):
            for yr in range(ys):
                if board[xr, yr]:
                    self[x + xr, yr + y] = True

    @override
    def __str__(self) -> str:
        return _board_to_str(self, None, trim_empty=False)


F, T = False, True

ROCKS = [
    Piece(i, Board.from_(form))
    for i, form in enumerate(
        [
            [
                [T, T, T, T],
            ],
            [
                [F, T, F],
                [T, T, T],
                [F, T, F],
            ],
            [
                [T, T, T],
                [F, F, T],
                [F, F, T],
            ],
            [
                [T],
                [T],
                [T],
                [T],
            ],
            [
                [T, T],
                [T, T],
            ],
        ]
    )
]


@dataclass
class Day17(BaseAdventDay[list[Jet]]):
    @override
    def parse_input(self) -> list[Jet]:
        cnt = count()

        def _tr(c: str) -> Jet:
            i = next(cnt)
            match c:
                case ">":
                    return Jet(i, Direction.Right)
                case "<":
                    return Jet(i, Direction.Left)
                case _:
                    raise ValueError("Invalid")

        return [_tr(c) for line in self.input for c in line.strip()]

    @override
    def _run_1(self, input: list[Jet]):
        return self._drop_rocks(input, 2022)

    @override
    def _run_2(self, input: list[Jet]):
        return self._drop_rocks(input, 1000000000000)

    def _drop_rocks(self, jet_list: list[Jet], rock_count: int) -> int:
        board = Board(7)
        height = 0
        jets = cycle(jet_list)
        rocks = cycle(ROCKS)

        states: dict[tuple[int, int, int], tuple[int, int]] = {}
        jet = None

        for rock_num in range(rock_count):
            rock = next(rocks)

            x = 2
            y = height + 3
            board.ensure_rows(y + rock.shape[1])

            _print(board, (rock, x, y), "START")
            stop = False

            while not stop:
                jet = next(jets)

                match jet.direction:
                    case Direction.Left if board.can_move_left(rock, x, y):
                        x -= 1
                    case Direction.Right if board.can_move_right(rock, x, y):
                        x += 1
                    case _:
                        pass

                _print(board, (rock, x, y), jet.direction.name.upper())

                # check if the rock collides down
                if board.can_move_down(rock, x, y):
                    y -= 1
                    _print(board, (rock, x, y), "DOWN")
                else:
                    stop = True

            board.apply(rock.board, x, y)

            height = max(height, y + rock.shape[1])
            _print(board, None, f"FINISH (height={height})")

            assert jet is not None
            state = (jet.index, rock.index, x)
            if prev := states.get(state):
                rocks_in_cycle = rock_num - prev[0]
                height_delta = height - prev[1]
                rock_remaining = rock_count - rock_num - 1
                cycles, remainder = divmod(rock_remaining, rocks_in_cycle)
                if remainder == 0:
                    return height_delta * cycles + height
            else:
                states[state] = (rock_num, height)

        return height


def _print(board: Board, rockT: tuple[Piece, int, int] | None, msg: str):
    if not PRINT:
        return

    print(msg)
    print(_board_to_str(board, rockT))


def _board_to_str(
    board: Board, rockT: tuple[Piece, int, int] | None, trim_empty: bool = True
) -> str:
    if rockT is not None:
        has_rock = True
        rock, xp, yp = rockT
        ps = rock.shape
        xr = range(xp, xp + ps[0])
        yr = range(yp, yp + ps[1])

        def ok(x: int, y: int) -> bool:
            return x in xr and y in yr and rock.board[x - xp, y - yp]
    else:
        has_rock = False

        def ok(x: int, y: int) -> bool:
            return False

    ret: list[str] = []

    for y in range(len(board) - 1, -1, -1):
        row = ["│"]
        empty = True
        for x in range(board.cols):
            sharp = board[x, y]
            at = has_rock and ok(x, y)
            try:
                assert {sharp, at} != {True}
            except AssertionError:
                raise

            if sharp:
                empty = False
                row.append("#")
            elif at:
                empty = False
                row.append("@")
            else:
                row.append(".")

        row.append("│")

        if not empty:
            trim_empty = False

        if not trim_empty:
            ret.append("".join(row))

    s = "─" * board.cols
    ret.append(f"└{s}┘")
    return "\n".join(ret)
