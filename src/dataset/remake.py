import os
from core.helpers import LoggerHelper
from vision.dataset import AgrismartRemakeDataset, AgrismartOriginalDataset
from vision.constants import VisionConstants

# uv run dataset --executor remake


def remake(**kwargs) -> None:
    LoggerHelper.print_full_width("STARTING REMAKE")

    remake_directory = VisionConstants.REMAKE_DIRECTORY
    original_directory = VisionConstants.ORIGINAL_DIRECTORY

    remake_classnames = [
        "Bacterial Leaf Blight",
        "Brown Spot",
        "Leaf Blast",
        "Leaf Blight",
        "Leaf Scald",
        "Leaf Smut",
        "Narrow Brown Spot",
    ]

    dataset = AgrismartRemakeDataset(remake_directory, remake_classnames)
    dataset.remake(original_directory)

    LoggerHelper.print_full_width("END REMAKE")
