import os
from enum import Enum


class DatasetMode(Enum):
    TRAIN = "train"
    VALIDATION = "val"
    TEST = "test"


class AgrismartDataset:
    def __init__(self, dataset_directory):
        if dataset_directory is None:
            raise ValueError("Please provide path to Agrismart dataset directory 🐳")

        self.dataset_directory = dataset_directory
        self.class_names = [
            "Bacterial Leaf Blight",
            "Brown Spot",
            "Healthy",
            "Leaf Blast",
            "Leaf Blight",
            "Leaf Scald",
            "Leaf Smut",
            "Narrow Brown Spot"
        ]

        self.validate()

    def validate(self):
        self.statistics(mode=DatasetMode.TRAIN)
        self.statistics(mode=DatasetMode.VALIDATION)
        self.statistics(mode=DatasetMode.TEST)

    def statistics(self, mode: DatasetMode = DatasetMode.TRAIN) -> None:
        print(f"==================================== Mode: {mode.value.upper()} ====================================")
        images_path = os.path.join(self.dataset_directory, mode.value, "images")
        labels_path = os.path.join(self.dataset_directory, mode.value, "labels")

        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            raise FileNotFoundError(f"Dataset directory for mode '{mode.value}' does not exist.")

        # Check image mapping with labels
        image_files = os.listdir(images_path)
        label_files = os.listdir(labels_path)

        if len(image_files) != len(label_files):
            raise ValueError("The number of images does not match the number of labels")

        objects = {
            i: {
                "bboxes": 0,
                "polygon": 0,
            } for i in range(len(self.class_names))
        }

        count_empty = 0

        for image_file in image_files:
            label_file = image_file.replace(".jpg", ".txt")
            if label_file not in label_files:
                print(f"Warning: not found label for image '{image_file}'")
            else:
                # read label and check following:
                # 1. if label is empty -> print warning
                # 2. if label contains
                #    - get class id and increment objects[class_id]
                #    - contains 2 format labels:
                #       - [class_id, x_center, y_center, width, height]
                #       - [class_id, x1, y1, x2, y2, x3, y3, ...]

                with open(os.path.join(labels_path, label_file), 'r') as f:
                    labels = f.readlines()

                if not labels:
                    print(f"Warning: label file '{label_file}' is empty")
                    count_empty += 1
                else:
                    for label in labels:
                        parts = label.strip().split()
                        class_id = int(parts[0])

                        if len(parts) < 5:
                            print(f"Warning: label file '{label_file}' has invalid format")
                            continue
                        elif len(parts) == 5:
                            # Format: [class_id, x_center, y_center, width, height]
                            objects[class_id]["bboxes"] += 1
                        else:
                            # Format: [class_id, x1, y1, x2, y2, ...]
                            objects[class_id]["polygon"] += 1

        print(f"Total images: {len(image_files)}")
        print(f"Total labels: {len(label_files)}")
        print(f"Empty labels: {count_empty}")
        print("Class statistics:")
        for class_id, stats in objects.items():
            print(f"Class '{self.class_names[class_id]}': {stats['bboxes']} bboxes, {stats['polygon']} polygons")
        print("=================================================================================================")
