import os
import cv2
from enum import Enum
import numpy as np
from vision.functions.drawing import Drawing
from typing import List
from .base_dataset import AgrismartBaseDataset, DatasetMode


class AgrismartOriginalDataset(AgrismartBaseDataset):
    def __init__(self, directory: str, classnames: List[str]) -> None:
        super().__init__(directory, classnames)

    def count_empty(self):
        total_empty = 0
        total_files = 0
        total_valid_file = 0

        for mode in DatasetMode:
            count = 0

            labels_path = os.path.join(self.directory, mode.value, "labels")
            label_files = os.listdir(labels_path)

            for label_file in label_files:
                label_path = os.path.join(labels_path, label_file)
                with open(label_path, "r") as file:
                    labels = file.readlines()

                if not labels:
                    count += 1

            print(f"Mode: {mode.value}, Empty labels count: {count}")
            print(f"Validation files: {len(label_files) - count}")
            total_empty += count
            total_files += len(label_files)
            total_valid_file += len(label_files) - count

        print(f"Total file: {total_files}")
        print(f"Total valid file: {total_valid_file}")
        print(f"Total empty labels count: {total_empty}")
