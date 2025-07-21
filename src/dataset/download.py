import os
import subprocess

from core.helpers import LoggerHelper


def download() -> None:
    LoggerHelper.print_full_width("STARTING DOWNLOAD")
    print("Please ensure you replace <your-key> with your actual Roboflow API key in the command below.")

    # 1. Check dataset exists, if not, create directory
    root_directory = os.getcwd()
    dataset_directory = os.path.join(root_directory, "datasets", "rice-leaf-disease")
    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory, exist_ok=True)
    else:
        print(f"Dataset directory {dataset_directory} already exists. Skipping creation.")
        LoggerHelper.print_full_width("END DOWNLOAD")
        return

    os.makedirs("datasets/rice-leaf-disease", exist_ok=True)

    # 2. Change directory & download
    command = (
        "cd datasets/rice-leaf-disease && "
        "curl -L 'https://universe.roboflow.com/ds/wMunxiKjaW?key=<your-key>' -o roboflow.zip && "
        "unzip roboflow.zip && rm roboflow.zip"
    )

    subprocess.run(command, shell=True, check=True)
    LoggerHelper.print_full_width("END DOWNLOAD")
