import os
import cv2
import numpy as np
from typing import Tuple, List
from numpy.typing import NDArray
from abc import ABC
from enum import Enum
from tabulate import tabulate
from core.helpers import LoggerHelper
from vision.functions.drawing import Drawing


class DatasetMode(Enum):
    TRAIN = "train"
    VALID = "valid"
    TEST = "test"

    @staticmethod
    def from_string(mode: str) -> "DatasetMode":
        try:
            return DatasetMode[mode.upper()]
        except KeyError:
            raise ValueError(f"Please choose mode available")


class AgrismartBaseDataset(ABC):
    def __init__(self, directory: str, classnames: List[str]):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not classnames:
            raise ValueError("Please provide a list of class names for this dataset.")

        self.classnames = classnames

    @staticmethod
    def reset_directory(path: str) -> None:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(path)

        # create new directory
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def convert_polygon_to_bbox(
            image: NDArray,
            coordinates: NDArray[np.float32],
            normalized: bool = True,
    ) -> Tuple[np.float32, np.float32, np.float32, np.float32]:
        """
        Convert polygon coordinates to bounding box format.
        Args:
            image: The image to which the polygon belongs.
            coordinates: Polygon coordinates in normalized format (x1, y1, x2, y2, ...).
            normalized: If True, return bounding box in normalized format (0-1 range).
        Returns:
            x_center, y_center, width, height: Bounding box coordinates.
        """
        h, w = image.shape[:2]

        points = []

        # noinspection PyTypeChecker
        for i in range(0, len(coordinates), 2):
            x_px = int(coordinates[i] * w)
            y_px = int(coordinates[i + 1] * h)
            points.append([x_px, y_px])

        x_min, y_min = np.min(points, axis=0)
        x_max, y_max = np.max(points, axis=0)

        width = x_max - x_min
        height = y_max - y_min

        x_center = x_min + width // 2
        y_center = y_min + height // 2

        if normalized:
            x_center /= w
            y_center /= h
            width /= w
            height /= h

        return x_center, y_center, width, height

    def statistics(
            self,
            dataset: str,
            mode: DatasetMode = DatasetMode.TRAIN,
    ) -> None:
        images_path = os.path.join(self.directory, mode.value, "images")
        labels_path = os.path.join(self.directory, mode.value, "labels")

        image_files = os.listdir(images_path)
        label_files = os.listdir(labels_path)

        if len(image_files) != len(label_files):
            raise ValueError("The number of images does not match the number of labels")

        # noinspection PyTypeChecker
        objects = {
            i: {"bboxes": 0, "polygon": 0, "files": 0}
            for i in range(len(self.classnames))
        }
        count_empty = 0

        for image_file in image_files:
            label_file = image_file.replace(".jpg", ".txt")

            if label_file not in label_files:
                print(f"Warning: not found label for image '{image_file}'")
                continue

            with open(os.path.join(labels_path, label_file), "r") as f:
                labels = f.readlines()

            if not labels:
                count_empty += 1
            else:
                class_id = None

                for label in labels:
                    parts = label.strip().split()
                    class_id = int(parts[0])

                    if len(parts) == 5:
                        # Format: [class_id, x_center, y_center, width, height]
                        objects[class_id]["bboxes"] += 1
                    else:
                        # Format: [class_id, x1, y1, x2, y2, ...]
                        objects[class_id]["polygon"] += 1

                if class_id is not None:
                    objects[class_id]["files"] += 1

        header = f"{mode.value.upper()} OF {dataset.upper()} DATASET"
        LoggerHelper.print_full_width(header)

        table = []
        for class_id, stats in objects.items():
            row = [
                self.classnames[class_id],
                stats["files"],
                stats["bboxes"],
                stats["polygon"],
                stats["bboxes"] + stats["polygon"],
            ]

            table.append(row)

        row = [
            "Total",
            sum(stats["files"] for stats in objects.values()),
            sum(stats["bboxes"] for stats in objects.values()),
            sum(stats["polygon"] for stats in objects.values()),
            sum(
                stats["bboxes"] + stats["polygon"] for stats in objects.values()
            ),
        ]
        table.append(row)

        print(
            tabulate(
                table,
                headers=["Class", "Files", "BBoxes", "Polygons", "Total"],
                tablefmt="pretty",
            )
        )
        print(
            f"Total images: {len(image_files)}, labels: {len(label_files)}, empty labels: {count_empty}"
        )

        # import cv2
        # import numpy as np
        #
        # # Read First Image
        # img1 = cv2.imread('GFG.png')
        #
        # # Read Second Image
        # img2 = cv2.imread('GFG.png')
        #
        # # concatenate image Horizontally
        # Hori = np.concatenate((img1, img2), axis=1)
        #
        # # concatenate image Vertically
        # Verti = np.concatenate((img1, img2), axis=0)
        #
        # cv2.imshow('HORIZONTAL', Hori)
        # cv2.imshow('VERTICAL', Verti)
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def show_single_sample(
            self,
            image_file,
            image,
            label_file,
            labels,
    ):
        drawing = Drawing(self.classnames)
        for label in labels:
            parts = label.strip().split()

            if len(parts) < 5:
                continue
            elif len(parts) == 5:
                # Bounding box format
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

                image = drawing.draw_bounding_box(
                    image, class_id, x_center, y_center, width, height
                )
            else:
                class_id = int(parts[0])
                coordinates = [float(coord) for coord in parts[1:]]

                image = drawing.draw_polygon(image, class_id, coordinates)

        cv2.imshow(f"Annotated: {image_file}", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_sample(
            self,
            mode: DatasetMode = DatasetMode.TRAIN,
            num_sample=None
    ) -> None:
        images_path = os.path.join(self.directory, mode.value, "images")
        labels_path = os.path.join(self.directory, mode.value, "labels")

        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            raise FileNotFoundError(
                f"Dataset directory for mode '{mode.value}' does not exist."
            )

        image_files = os.listdir(images_path)
        label_files = os.listdir(labels_path)

        drawing = Drawing(self.classnames)
        images_show = []
        skip_count = 0

        for image_file in image_files[:num_sample]:
            label_file = image_file.replace(".jpg", ".txt")
            if label_file not in label_files:
                print(f"Warning: No label found for image '{image_file}'. Skipping.")
                skip_count += 1
                continue

            # read image
            image_path = os.path.join(images_path, image_file)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Error reading image '{image_file}'. Skipping.")
                skip_count += 1
                continue

            # read label
            label_path = os.path.join(labels_path, label_file)
            with open(label_path, "r") as file:
                labels = file.readlines()

            if not labels:
                print(f"Warning: label file '{label_file}' is empty. Skipping.")
                skip_count += 1
                continue

            print(f"Processing image: {image_file}")
            for label in labels:
                parts = label.strip().split()

                if len(parts) < 5:
                    print(
                        f"Warning: label file '{label_file}' has invalid format. Skipping."
                    )
                    skip_count += 1
                    continue
                elif len(parts) == 5:
                    # Bounding box format
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    image = drawing.draw_bounding_box(
                        image, class_id, x_center, y_center, width, height
                    )
                else:
                    class_id = int(parts[0])
                    coordinates = [float(coord) for coord in parts[1:]]

                    image = drawing.draw_polygon(image, class_id, coordinates)

            # cv2.imshow(f"Annotated: {image_file}", image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            images_show.append({
                "file": image_file,
                "image": image
            })

        # Concatenate images horizontally 5 file and vertically 2 files
        for i in range(0, 100, 10):
            if i + 10 <= len(images_show):
                items1 = images_show[i:i + 5]
                items2 = images_show[i + 5:i + 10]

                row1 = [item["image"] for item in items1]
                row2 = [item["image"] for item in items2]

                row1_concat = np.concatenate(row1, axis=1)
                row2_concat = np.concatenate(row2, axis=1)
                combined_image = np.concatenate((row1_concat, row2_concat), axis=0)

                for item in items1:
                    print(f"Image: {item['file']}")

                for item in items2:
                    print(f"Image: {item['file']}")

                cv2.imshow(f"Sample {i // 10 + 1}", combined_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                pass
                # row1 = images_show[i:len(images_show)]
                # row1_concat = np.concatenate(row1, axis=1)
                #
                # cv2.imshow(f"Sample {i // 10 + 1}", row1_concat)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

        print(f"Displayed {len(images_show)} images with annotations.")
        print(f"Skipped {skip_count} images due to missing labels or read errors.")
