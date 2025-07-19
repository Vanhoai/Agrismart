import os
import cv2
from enum import Enum
import numpy as np
from numpy.typing import NDArray
from typing import Tuple
from .drawing import Drawing


class DatasetMode(Enum):
    TRAIN = "train"
    VALIDATION = "val"
    TEST = "test"


class AgrismartDataset:
    def __init__(self, dataset_directory, remake_directory, is_validate: bool = True):
        if dataset_directory is None:
            raise ValueError("Please provide path to Agrismart dataset directory 🐳")

        if remake_directory is None:
            raise ValueError("Please provide path to remake directory 🐳")

        self.dataset_directory = dataset_directory
        self.remake_directory = remake_directory
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

        if is_validate:
            self.validate()

    def validate(self, dataset="original") -> None:
        self.statistics(mode=DatasetMode.TRAIN, dataset=dataset)
        self.statistics(mode=DatasetMode.VALIDATION, dataset=dataset)
        self.statistics(mode=DatasetMode.TEST, dataset=dataset)

    def statistics(
            self,
            dataset="original",
            mode: DatasetMode = DatasetMode.TRAIN
    ) -> None:
        directory = self.dataset_directory if dataset == "original" else self.remake_directory

        print(f"==================================== Mode: {mode.value.upper()} ====================================")
        print(f"Dataset directory: {directory}")
        images_path = os.path.join(directory, mode.value, "images")
        labels_path = os.path.join(directory, mode.value, "labels")

        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            raise FileNotFoundError(f"Dataset directory for mode '{mode.value}' does not exist.")

        # Check image mapping with labels
        image_files = os.listdir(images_path)
        label_files = os.listdir(labels_path)

        print(f"Total images: {len(image_files)}")
        print(f"Total labels: {len(label_files)}")

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
                    # print(f"Warning: label file '{label_file}' is empty")
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
        print("=================================================================================================\n")

    def show_sample(
            self,
            dataset="original",
            mode: DatasetMode = DatasetMode.TRAIN,
            num_sample=10
    ) -> None:
        directory = self.dataset_directory if dataset == "original" else self.remake_directory

        images_path = os.path.join(directory, mode.value, "images")
        labels_path = os.path.join(directory, mode.value, "labels")

        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            raise FileNotFoundError(f"Dataset directory for mode '{mode.value}' does not exist.")

        image_files = os.listdir(images_path)
        label_files = os.listdir(labels_path)

        drawing = Drawing(self.class_names)

        for image_file in image_files[:num_sample]:
            label_file = image_file.replace(".jpg", ".txt")
            if label_file not in label_files:
                print(f"Warning: No label found for image '{image_file}'. Skipping.")
                continue

            # read image
            image_path = os.path.join(images_path, image_file)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Error reading image '{image_file}'. Skipping.")
                continue

            # read label
            label_path = os.path.join(labels_path, label_file)
            with open(label_path, "r") as file:
                labels = file.readlines()

            if not labels:
                print(f"Warning: label file '{label_file}' is empty. Skipping.")
                continue

            print(f"Processing image: {image_file}")
            for label in labels:
                parts = label.strip().split()
                if len(parts) < 5:
                    print(f"Warning: label file '{label_file}' has invalid format. Skipping.")
                    continue

                if len(parts) < 5:
                    print(f"Warning: label file '{label_file}' has invalid format. Skipping.")
                    continue
                elif len(parts) == 5:
                    # Bounding box format
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                    image = drawing.draw_bounding_box(image, class_id, x_center, y_center, width, height)
                else:
                    # Polygon segmentation format
                    class_id = int(parts[0])
                    coords = [float(coord) for coord in parts[1:]]

                    image = drawing.draw_polygon(image, class_id, coords)

            cv2.imshow(f"Annotated: {image_file}", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        cv2.destroyAllWindows()

    def convert_polygon_to_bbox(
            self,
            image,
            coords: NDArray[np.float32],
            normalized: bool = True
    ) -> Tuple[np.float32, np.float32, np.float32, np.float32]:
        """
        Convert polygon points to bounding box coordinates.
        Params:
            points (np.ndarray): Array of shape (N, 2) where N is the number of points.
        Returns:
            Tuple[int, int, int, int]: (x_center, y_center, width, height)
        """
        h, w = image.shape[:2]

        points = []
        for i in range(0, len(coords), 2):
            x_px = int(coords[i] * w)
            y_px = int(coords[i + 1] * h)
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

    def remake(self) -> None:
        """
        Remake the dataset by converting polygon annotations to bounding boxes.
        This function will read the original dataset, convert polygon annotations
        to bounding boxes, and save them in the remake directory.

        Following steps are performed:
        1. Create remake directory structure
        2. For each mode (train, val, test):
            for each image in the mode:
                read image and label
                if label is empty
                    if name file contain "Healthy"
                        skip (healthy class)
                    else
                        copy image and label to remake directory

                if label have class id is 2
                    skip (healthy class)
                else
                    if label is polygon format:
                        convert polygon to bounding box
                        save bounding box in remake directory
                    else:
                        copy image and label to remake directory

        Note:
        - The remake directory will be created if it does not exist.
        - Class id 2 is considered as "Healthy" class and will be skipped.
        - When label copy to remake directory, it will be decreased by 1 if class id is greater than 2.
        """
        print("================================== REMAKING DATASET ==================================")

        # if remake_directory exists, remove it
        self.reset_directory(self.remake_directory)

        # count_skipped = 0
        # for mode in DatasetMode:
        #     images_path = os.path.join(self.dataset_directory, mode.value, "images")
        #     labels_path = os.path.join(self.dataset_directory, mode.value, "labels")
        #
        #     remake_images_path = os.path.join(self.remake_directory, mode.value, "images")
        #     remake_labels_path = os.path.join(self.remake_directory, mode.value, "labels")
        #
        #     os.makedirs(remake_images_path, exist_ok=True)
        #     os.makedirs(remake_labels_path, exist_ok=True)
        #
        #     image_files = os.listdir(images_path)
        #     label_files = os.listdir(labels_path)
        #
        #     for image_file in image_files:
        #         label_file = image_file.replace(".jpg", ".txt")
        #         if label_file not in label_files:
        #             print(f"Warning: No label found for image '{image_file}'. Skipping.")
        #             count_skipped += 1
        #             continue
        #
        #         # read image
        #         image_path = os.path.join(images_path, image_file)
        #         copy_image = cv2.imread(image_path)
        #         if copy_image is None:
        #             print(f"Error reading image '{image_file}'. Skipping.")
        #             count_skipped += 1
        #             continue
        #
        #         # read label
        #         label_path = os.path.join(labels_path, label_file)
        #         with open(label_path, "r") as file:
        #             labels = file.readlines()
        #
        #         if not labels:
        #             if image_file.lower().startswith("healthy"):
        #                 print(f"Skipping healthy image '{image_file}' with empty label.")
        #                 count_skipped += 1
        #                 continue
        #             else:
        #                 if skip_empty:
        #                     print(f"Skipping image '{image_file}' with empty label.")
        #                     count_skipped += 1
        #                     continue
        #
        #                 # Copy image and label to remake directory
        #                 cv2.imwrite(os.path.join(remake_images_path, image_file), copy_image)
        #                 with open(os.path.join(remake_labels_path, label_file), "w") as f:
        #                     f.write("")
        #                 print(f"Copied empty label for image '{image_file}' to remake directory.")
        #                 continue
        #         else:
        #             if image_file.lower().startswith("healthy"):
        #                 print(f"Skipping healthy image '{image_file}' with non-empty label.")
        #                 count_skipped += 1
        #                 continue
        #
        #             with open(os.path.join(remake_labels_path, label_file), "w") as f:
        #                 for label in labels:
        #                     parts = label.strip().split()
        #                     class_id = int(parts[0])
        #
        #                     if class_id == 2:
        #                         print(
        #                             f"Skipping healthy class '{self.class_names[class_id]}' for image '{image_file}'.")
        #                         count_skipped += 1
        #                         continue
        #                     elif len(parts) < 5:
        #                         print(f"Warning: label file '{label_file}' has invalid format. Skipping.")
        #                         count_skipped += 1
        #                         continue
        #                     elif len(parts) == 5:
        #                         # Bounding box format
        #                         x_center = float(parts[1])
        #                         y_center = float(parts[2])
        #                         width = float(parts[3])
        #                         height = float(parts[4])
        #
        #                         # Write bounding box to remake label file
        #                         new_class_id = class_id - 1 if class_id > 2 else class_id
        #                         f.write(f"{new_class_id} {x_center} {y_center} {width} {height}\n")
        #                         print(f"Copied label with bbox format for image '{image_file}' to remake directory.")
        #                     else:
        #                         # Polygon format
        #                         coord = [float(coord) for coord in parts[1:]]
        #                         x_center, y_center, width, height = self.convert_polygon_to_bbox(
        #                             copy_image,
        #                             np.array(coord),
        #                         )
        #
        #                         # Write bounding box to remake label file
        #                         new_class_id = class_id - 1 if class_id > 2 else class_id
        #                         f.write(f"{new_class_id} {x_center} {y_center} {width} {height}\n")
        #                         print(f"Copied label with polygon format for image '{image_file}' to remake directory.")
        #
        #             # Save the image in the remake directory
        #             cv2.imwrite(os.path.join(remake_images_path, image_file), copy_image)
        #
        # print("======================================================================================")
        # print("Remake completed successfully! 🎉")
        # print("Dataset has been converted to bounding boxes and saved in the remake directory.")
        # print(f"Please check directory {self.remake_directory}")
        # print(f"Total skipped images: {count_skipped}")
        # print("======================================================================================")
