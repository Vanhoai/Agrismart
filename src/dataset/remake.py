import os
from core.helpers import LoggerHelper
from vision.datasets import AgrismartRemakeDataset, AgrismartOriginalDataset


# uv run dataset --executor statistics --dataset original --modes "train valid test"
# uv run dataset --executor remake

# 584


def remake(**kwargs) -> None:
    LoggerHelper.print_full_width("STARTING REMAKE")

    root_directory = os.getcwd()
    directory = os.path.join(root_directory, "datasets", "remake")
    original_directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")

    classnames = [
        "Bacterial Leaf Blight",
        "Brown Spot",
        "Healthy",
        "Leaf Blast",
        "Leaf Blight",
        "Leaf Scald",
        "Leaf Smut",
        "Narrow Brown Spot",
    ]

    dataset = AgrismartRemakeDataset(directory, classnames)
    dataset.remake(original_directory)

    LoggerHelper.print_full_width("END REMAKE")
