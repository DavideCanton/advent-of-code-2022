from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cached_property
from itertools import cycle
from typing import Self, override

from advent.common import BaseAdventDay

PRINT = False
WAIT = False


class Direction(Enum):
    Left = auto()
    Right = auto()


type Form = list[list[bool]]


@dataclass
class Piece:
    form: Board

    @cached_property
    def shape(self) -> tuple[int, int]:
        return self.form.shape


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
                if rock.form[xr, yr] and self[x - 1 + xr, yr + y]:
                    return False

        return True

    def can_move_right(self, rock: Piece, x: int, y: int) -> bool:
        if x == self.cols - rock.shape[0]:
            return False

        for xr in range(rock.shape[0]):
            for yr in range(rock.shape[1]):
                if rock.form[xr, yr] and self[x + 1 + xr, yr + y]:
                    return False

        return True

    def can_move_down(self, rock: Piece, x: int, y: int) -> bool:
        if y == 0:
            return False

        for xr in range(rock.shape[0]):
            for yr in range(rock.shape[1]):
                if rock.form[xr, yr] and self[x + xr, yr - 1 + y]:
                    return False

        return True

    @override
    def __str__(self) -> str:
        return _board_to_str(self, None, trim_empty=False)


F, T = False, True

PIECES = [
    Piece(Board.from_(form))
    for form in [
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
]


@dataclass
class Day17(BaseAdventDay[list[Direction]]):
    @override
    def parse_input(self) -> list[Direction]:
        def _tr(c: str) -> Direction:
            match c:
                case ">":
                    return Direction.Right
                case "<":
                    return Direction.Left
                case _:
                    raise ValueError("Invalid")

        return [_tr(c) for line in self.input for c in line.strip()]

    @override
    def _run_1(self, input: list[Direction]):
        return self._do(input, 2022)

    @override
    def _run_2(self, input: list[Direction]):
        return self._do(input, 1000000000000)

    def _do(self, dir_input: list[Direction], rock_count: int) -> int:
        board = Board(7)
        last = 0
        rocks = cycle(PIECES)
        dirs = cycle(dir_input)

        for _ in range(rock_count):
            rock = next(rocks)
            x = 2
            y = last + 3
            board.ensure_rows(y + rock.shape[1])

            _print(board, (rock, x, y), "START")
            stop = False

            while not stop:
                dir = next(dirs)
                if dir == Direction.Left:
                    if board.can_move_left(rock, x, y):
                        x -= 1
                elif dir == Direction.Right:
                    if board.can_move_right(rock, x, y):
                        x += 1

                _print(board, (rock, x, y), dir.name.upper())

                stop = False

                # check if the rock collides down (y==0 checked by can_move_down)
                if not board.can_move_down(rock, x, y):
                    stop = True
                    break

                # if no stop is reached, move down
                if not stop:
                    y -= 1
                    _print(board, (rock, x, y), "DOWN")

            for yp, ll in enumerate(rock.form.board):
                for xp, v in enumerate(ll):
                    if v:
                        board[x + xp, y + yp] = True

            last = max(last, y + rock.shape[1])
            _print(board, None, f"FINISH (last={last})")
            if WAIT:
                input()

        return last


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
            return x in xr and y in yr and rock.form[x - xp, y - yp]
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
