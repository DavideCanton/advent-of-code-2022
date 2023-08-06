import argparse
from pathlib import Path

import pdbp  # noqa: F401

from advent import CLASSES


def create_parser():
    parser = argparse.ArgumentParser(description="Advent of code runner.")

    parser.add_argument(
        "day",
        help="The day to run, 1 to 25.",
        choices=list(range(1, 26)),
        type=int,
        metavar="DAY",
    )
    parser.add_argument(
        "var",
        help="The variant of the day, 1 to 2, defaults to 1.",
        default=1,
        metavar="VAR",
        type=int,
        nargs="?",
        choices=[1, 2],
    )
    parser.add_argument(
        "-f", "--file", metavar="INPUT", type=str, nargs="?", help="Override file path"
    )
    return parser


def main():
    args = create_parser().parse_args()
    day = args.day
    try:
        cls = CLASSES[args.day]
    except KeyError:
        print("Module not yet implemented!")
    else:
        if args.file is None:
            input_folder = Path(__file__).parent / "inputs"
            file_path = input_folder / f"day{day}.txt"
        else:
            file_path = Path(args.file)
        res = cls(file_path).run(args.var)
        print(f"Result for day {args.day}, variant {args.var}, is:")
        print(res)


if __name__ == "__main__":
    main()
