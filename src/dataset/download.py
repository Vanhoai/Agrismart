import os
import subprocess

from vision.constants import VisionConstants
from core.helpers import LoggerHelper
from core.configuration import Configuration


def download() -> None:
    """
    Downloads the original rice leaf diseases dataset from Roboflow.
    Ensure you have set your Roboflow API key in the .env file under the key `ROBOFLOW_KEY`.
    The dataset will be downloaded into the directory specified by `VisionConstants.ORIGINAL_DIRECTORY`.
    If the directory already exists, it will skip the download.

    Usage:
        uv run dataset --executor download
    Note:
        Make sure to replace `<your-key>` with your actual Roboflow API key in the `.env` file.
    """
    config = Configuration()
    LoggerHelper.print_full_width("STARTING DOWNLOAD")
    print("Please ensure you replace <your-key> with your actual Roboflow API key.")

    # 1. Check dataset exists, if not, create directory
    dataset_directory = VisionConstants.ORIGINAL_DIRECTORY

    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory, exist_ok=True)
    else:
        print(f"Dataset directory already exists. Skipping creation.")
        LoggerHelper.print_full_width("END DOWNLOAD")
        return

    os.makedirs(VisionConstants.ORIGINAL_DIRECTORY, exist_ok=True)

    # 2. Change directory & download
    command = (
        f"cd {VisionConstants.ORIGINAL_DIRECTORY} && "
        f"curl -L 'https://universe.roboflow.com/ds/wMunxiKjaW?key={config.ROBOFLOW_KEY}' -o roboflow.zip && "
        "unzip roboflow.zip && rm roboflow.zip"
    )

    subprocess.run(command, shell=True, check=True)
    LoggerHelper.print_full_width("END DOWNLOAD")
