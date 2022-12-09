import argparse
import importlib


def create_parser():
    parser = argparse.ArgumentParser(description="Advent of code runner.")

    parser.add_argument(
        "day", help="The day to run", choices=list(range(1, 26)), type=int
    )
    parser.add_argument(
        "var",
        help="The variant of the day",
        default=1,
        type=int,
        choices=list(range(1, 3)),
    )
    return parser


def main():
    args = create_parser().parse_args()
    module = importlib.import_module(f"day{args.day}")
    module.run(args.var)


if __name__ == "__main__":
    main()
