import os

from core.helpers import LoggerHelper
from vision.datasets import AgrismartOriginalDataset, AgrismartRemakeDataset, DatasetMode


def statistics(**kwargs) -> None:
    LoggerHelper.print_full_width("STARTING STATISTICS")

    root_directory = os.getcwd()
    modes = kwargs.get("modes", "train valid").split()

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
        original_directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")
        remake_directory = os.path.join(root_directory, "datasets", "remake")

        original_dataset = AgrismartOriginalDataset(directory=original_directory, classnames=original_classnames)
        remake_dataset = AgrismartRemakeDataset(directory=remake_directory, classnames=remake_classnames)

        if not os.path.exists(remake_directory):
            raise FileNotFoundError(remake_directory)

        if not os.path.exists(original_directory):
            raise FileNotFoundError(original_directory)

        for mode in modes:
            mode_enum = DatasetMode.from_string(mode)
            original_dataset.statistics("ORIGINAL", mode=mode_enum)
            remake_dataset.statistics("REMAKE", mode=mode_enum)

        LoggerHelper.print_full_width("END STATISTICS")
        return

    if kwargs["dataset"] == "original":
        directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")
        if not os.path.exists(directory):
            raise FileNotFoundError(directory)

        dataset = AgrismartOriginalDataset(directory=directory, classnames=original_classnames)
    else:
        directory = os.path.join(root_directory, "datasets", "remake")
        if not os.path.exists(directory):
            raise FileNotFoundError(directory)

        dataset = AgrismartRemakeDataset(directory=directory, classnames=remake_classnames)

    for mode in modes:
        mode_enum = DatasetMode.from_string(mode)
        dataset.statistics(mode=mode_enum, dataset=kwargs["dataset"].upper())

    LoggerHelper.print_full_width("END STATISTICS")
