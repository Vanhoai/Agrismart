import sys
import argparse

from .download import download
from .show import show
from .remake import remake
from .statistics import statistics


def main() -> None:
    parser = argparse.ArgumentParser(description="Process dataset commands.")
    parser.add_argument(
        "--executor",
        choices=["download", "remake", "statistics", "show"],
        help="Executor to run: download, remake, statistics, or show",
    )

    parser.add_argument(
        "--dataset",
        type=str,
        default="original",
        choices=["original", "remake", "all"],
        help="Dataset type to use: original or remake",
    )

    parser.add_argument(
        "--modes",
        type=str,
        default="train valid",
        help="Mode to run: train, valid, test",
    )

    parser.add_argument(
        "--num",
        type=int,
        default=100,
        help="Number of samples to show (only for show command)",
    )

    args = parser.parse_args()
    match args.executor:
        case "download":
            download()
        case "remake":
            remake()
        case "statistics":
            statistics(dataset=args.dataset, modes=args.modes)
        case "show":
            show(dataset=args.dataset, modes=args.modes, num=args.num)
        case _:
            print(
                "Please choose a available mode: download, remake, statistics, or show."
            )
            sys.exit(1)
