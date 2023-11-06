from pathlib import Path
from typing import Literal

import click
import pdbp

from advent import CLASSES
from advent.common import ResultProtocol

pdbp.enable()


def _run(day: int, var: Literal[1, 2], file: Path | None) -> ResultProtocol:
    try:
        cls = CLASSES[day]
    except KeyError as e:
        raise ValueError("Module not yet implemented!") from e
    else:
        if file is None:
            input_folder = Path(__file__).parent / "inputs"
            file_path = input_folder / f"day{day}.txt"
        else:
            file_path = file
        return cls(file_path).run(var)


@click.command(
    help="Advent of code runner. Specify a DAY from 1 to 25 and a variant (1/2), default 1."
)
@click.argument("day", type=click.IntRange(1, 25))
@click.argument("var", type=click.IntRange(1, 2), default=1)
@click.option(
    "-f",
    "--file",
    help="Override file path",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
)
def run(day: int, var: Literal[1, 2], file: Path | None) -> ResultProtocol:
    res = _run(day, var, file)
    print(f"Result for day {day}, variant {var}, is:")
    print(res)


if __name__ == "__main__":
    run()
