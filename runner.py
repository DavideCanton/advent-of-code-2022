import argparse
from pathlib import Path

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
        choices=list(range(1, 3)),
    )
    return parser


def main():
    args = create_parser().parse_args()
    try:
        cls = CLASSES[args.day]
    except KeyError:
        print("Module not yet implemented!")
    else:
        input_folder = Path(__file__).parent / "inputs"
        res = cls(input_folder).run(args.var)
        print(f"Result for day {args.day}, variant {args.var}, is:")
        print(res)


if __name__ == "__main__":
    main()
