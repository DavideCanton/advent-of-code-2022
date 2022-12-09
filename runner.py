import argparse
import importlib


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
        module = importlib.import_module(f"advent.day{args.day}")
    except ImportError:
        print("Module not yet implemented!")
    else:
        res = module.Instance.run(args.var)
        print(f"Result for day {args.day}, variant {args.var}, is {res}.")


if __name__ == "__main__":
    main()
