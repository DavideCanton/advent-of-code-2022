from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from itertools import cycle
from typing import override

from advent.common import BaseAdventDay

PRINT = False


class Direction(Enum):
    Left = 1
    Right = 2


@dataclass
class Piece:
    form: list[list[bool]]

    @cached_property
    def shape(self) -> tuple[int, int]:
        return len(self.form), len(self.form[0])


F, T = False, True

PIECES = [
    Piece(form)
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
            [F, F, T],
            [F, F, T],
            [T, T, T],
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

    def _do(self, input: list[Direction], rock_count: int) -> int:
        w = 7
        board = [[False] * w]
        last = -1
        rocks = cycle(PIECES)
        dirs = cycle(input)

        for _ in range(rock_count):
            rock = next(rocks)
            x = 2
            y = last + 3 + rock.shape[0]

            for _ in range(y + 1 - len(board)):
                board.append([False] * w)

            _print(board, rock, x, y, "START")
            stop = False

            while not stop:
                dir = next(dirs)
                if dir == Direction.Left and x > 0:
                    if not any(
                        v and board[y - yi][x - 1] for yi, v in enumerate(r[0] for r in rock.form)
                    ):
                        x -= 1
                elif dir == Direction.Right and x + rock.shape[1] < w:
                    if not any(
                        v and board[y - yi][x + rock.shape[1]]
                        for yi, v in enumerate(r[-1] for r in rock.form)
                    ):
                        x += 1

                _print(board, rock, x, y, dir.name.upper())

                # if last row reached, stop
                stop = y == rock.shape[0] - 1

                # else check if the rock collides down
                if not stop:
                    ys = y - rock.shape[0]
                    for xi, r in enumerate(rock.form[-1]):
                        if r and board[ys][x + xi]:
                            stop = True
                            break

                # if no stop is reached, move down
                if not stop:
                    y -= 1
                    _print(board, rock, x, y, "DOWN")

            for yp, ll in enumerate(rock.form):
                for xp, v in enumerate(ll):
                    if v:
                        board[y - yp][x + xp] = True

            last = max(last, y)
            _print(board, rock, x, y, "FINISH")

        return last + 1


type Func[**P] = Callable[P, None]


def bypass[**P](run: bool) -> Callable[[Func[P]], Func[P]]:
    def inner(func: Func[P]) -> Func[P]:
        if run:
            return func
        else:

            def noop(*args: P.args, **kwargs: P.kwargs) -> None:
                pass

            return noop

    return inner


@bypass(PRINT)
def _print(
    board: list[list[bool]],
    rock: Piece,
    xp: int,
    yp: int,
    msg: str,
):
    print(msg)
    ps = rock.shape
    xr = range(xp, xp + ps[1])
    yr = range(yp, yp - ps[0], -1)

    for y in reversed(range(len(board))):
        for x in range(7):
            if board[y][x]:
                print("#", end="")
            elif x in xr and y in yr and rock.form[yp - y][x - xp]:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print()
