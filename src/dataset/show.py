from core.helpers import LoggerHelper
from vision.dataset import AgrismartOriginalDataset, DatasetMode, AgrismartRemakeDataset
from vision.constants import VisionConstants

# uv run dataset --executor show --dataset remake --modes "train" --num 100
# uv run dataset --executor show --dataset original --modes "train" --num 100


def show(**kwargs) -> None:
    if kwargs["dataset"] == "all":
        raise ValueError("Option 'all' is not supported for show command.")

    LoggerHelper.print_full_width("STARTING SHOW")
    dataset = None
    if kwargs["dataset"] == "original":
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
        dataset_directory = VisionConstants.ORIGINAL_DIRECTORY
        dataset = AgrismartOriginalDataset(dataset_directory, classnames)

    elif kwargs["dataset"] == "remake":
        classnames = [
            "Bacterial Leaf Blight",
            "Brown Spot",
            "Leaf Blast",
            "Leaf Blight",
            "Leaf Scald",
            "Leaf Smut",
            "Narrow Brown Spot",
        ]
        dataset_directory = VisionConstants.REMAKE_DIRECTORY
        dataset = AgrismartRemakeDataset(dataset_directory, classnames)

    modes = kwargs["modes"].split()
    if len(modes) > 1:
        raise ValueError("Multiple modes are not supported for show command.")

    mode = DatasetMode.from_string(modes[0])
    dataset.show_sample(mode, num_sample=kwargs.get("num", 100))  # type: ignore
    LoggerHelper.print_full_width("END SHOW")
