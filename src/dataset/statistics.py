import os

from core.helpers import LoggerHelper
from vision.dataset import AgrismartOriginalDataset, AgrismartRemakeDataset, DatasetMode
from vision.constants import VisionConstants

# uv run dataset --executor statistics --dataset original --modes "train valid test"
# uv run dataset --executor statistics --dataset original --modes "train"
# uv run dataset --executor statistics --dataset remake --modes "train"


def statistics(**kwargs) -> None:
    LoggerHelper.print_full_width("STARTING STATISTICS")
    modes = kwargs.get("modes", "train valid test").split()

    original_classnames = [
        "Bacterial Leaf Blight",
        "Brown Spot",
        "Healthy",
        "Leaf Blast",
        "Leaf Blight",
        "Leaf Scald",
        "Leaf Smut",
        "Narrow Brown Spot",
    ]

    remake_classnames = [
        "Bacterial Leaf Blight",
        "Brown Spot",
        "Leaf Blast",
        "Leaf Blight",
        "Leaf Scald",
        "Leaf Smut",
        "Narrow Brown Spot",
    ]

    if kwargs["dataset"] == "all":
        original_dataset = AgrismartOriginalDataset(
            directory=VisionConstants.ORIGINAL_DIRECTORY,
            classnames=original_classnames,
        )

        remake_dataset = AgrismartRemakeDataset(
            directory=VisionConstants.REMAKE_DIRECTORY,
            classnames=remake_classnames,
        )

        if not os.path.exists(VisionConstants.REMAKE_DIRECTORY):
            raise FileNotFoundError(VisionConstants.REMAKE_DIRECTORY)

        if not os.path.exists(VisionConstants.ORIGINAL_DIRECTORY):
            raise FileNotFoundError(VisionConstants.ORIGINAL_DIRECTORY)

        for mode in modes:
            mode_enum = DatasetMode.from_string(mode)
            original_dataset.statistics("ORIGINAL", mode=mode_enum)
            remake_dataset.statistics("REMAKE", mode=mode_enum)

        LoggerHelper.print_full_width("END STATISTICS")
        return

    if kwargs["dataset"] == "original":
        directory = VisionConstants.ORIGINAL_DIRECTORY

        if not os.path.exists(directory):
            raise FileNotFoundError(directory)

        dataset = AgrismartOriginalDataset(
            directory=directory,
            classnames=original_classnames,
        )
    else:
        directory = VisionConstants.REMAKE_DIRECTORY

        if not os.path.exists(directory):
            raise FileNotFoundError(directory)

        dataset = AgrismartRemakeDataset(
            directory=directory,
            classnames=remake_classnames,
        )

    for mode in modes:
        mode_enum = DatasetMode.from_string(mode)
        dataset.statistics(mode=mode_enum, dataset=kwargs["dataset"].upper())

    LoggerHelper.print_full_width("END STATISTICS")
