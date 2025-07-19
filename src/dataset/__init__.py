import sys
import argparse
import subprocess

from .download import download
from .show import show
from .remake import remake
from .statistics import statistics


def main() -> None:
    parser = argparse.ArgumentParser(description="Process dataset commands.")
    parser.add_argument(
        "mode",
        choices=["download", "remake", "statistics", "show"],
        help="Mode of operation"
    )
    parser.add_argument(
        "--set",
        type=str,
        default="train",
        choices=["train", "val", "test"],
        help="Set to operate on (default: train)"
    )

    args = parser.parse_args()
    match args.mode:
        case "download":
            download()
        case "remake":
            remake()
        case "statistics":
            statistics()
        case "show":
            show()
        case _:
            print("Please choose a available mode: download, remake, statistics, or show.")
            sys.exit(1)
