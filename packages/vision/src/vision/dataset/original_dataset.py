import os
import cv2
from enum import Enum
import numpy as np
from vision.functions.drawing import Drawing
from typing import List
from .base_dataset import AgrismartBaseDataset, DatasetMode


# Mode: train, Empty labels count: 44
# Validation files: 3850
# Mode: valid, Empty labels count: 5
# Validation files: 927
# Mode: test, Empty labels count: 4
# Validation files: 358

# Total file: 5188
# Total valid file: 5135
# Total empty labels count: 53


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

#
# class DatasetMode(Enum):
#     TRAIN = "train"
#     VALIDATION = "valid"
#     TEST = "test"
#
#
# class AgrismartDataset:
#     def __init__(self, dataset_directory, remake_directory, is_validate: bool = True):
#         if dataset_directory is None:
#             raise ValueError("Please provide path to Agrismart dataset directory 🐳")
#
#         if remake_directory is None:
#             raise ValueError("Please provide path to remake directory 🐳")
#
#         self.dataset_directory = dataset_directory
#         self.remake_directory = remake_directory
#         self.original_class_names = [
#             "Bacterial Leaf Blight",
#             "Brown Spot",
#             "Healthy",
#             "Leaf Blast",
#             "Leaf Blight",
#             "Leaf Scald",
#             "Leaf Smut",
#             "Narrow Brown Spot",
#         ]
#
#         self.remake_class_names = [
#             "Bacterial Leaf Blight",
#             "Brown Spot",
#             "Leaf Blast",
#             "Leaf Blight",
#             "Leaf Scald",
#             "Leaf Smut",
#             "Narrow Brown Spot",
#         ]
#
#     def show_sample(
#             self, dataset="original", mode: DatasetMode = DatasetMode.TRAIN, num_sample=10
#     ) -> None:
#         directory = (
#             self.dataset_directory if dataset == "original" else self.remake_directory
#         )
#
#         images_path = os.path.join(directory, mode.value, "images")
#         labels_path = os.path.join(directory, mode.value, "labels")
#
#         if not os.path.exists(images_path) or not os.path.exists(labels_path):
#             raise FileNotFoundError(
#                 f"Dataset directory for mode '{mode.value}' does not exist."
#             )
#
#         image_files = os.listdir(images_path)
#         label_files = os.listdir(labels_path)
#
#         drawing = Drawing(self.original_class_names)
#
#         for image_file in image_files[:num_sample]:
#             label_file = image_file.replace(".jpg", ".txt")
#             if label_file not in label_files:
#                 print(f"Warning: No label found for image '{image_file}'. Skipping.")
#                 continue
#
#             # read image
#             image_path = os.path.join(images_path, image_file)
#             image = cv2.imread(image_path)
#
#             if image is None:
#                 print(f"Error reading image '{image_file}'. Skipping.")
#                 continue
#
#             # read label
#             label_path = os.path.join(labels_path, label_file)
#             with open(label_path, "r") as file:
#                 labels = file.readlines()
#
#             if not labels:
#                 print(f"Warning: label file '{label_file}' is empty. Skipping.")
#                 continue
#
#             print(f"Processing image: {image_file}")
#             for label in labels:
#                 parts = label.strip().split()
#                 if len(parts) < 5:
#                     print(
#                         f"Warning: label file '{label_file}' has invalid format. Skipping."
#                     )
#                     continue
#
#                 if len(parts) < 5:
#                     print(
#                         f"Warning: label file '{label_file}' has invalid format. Skipping."
#                     )
#                     continue
#                 elif len(parts) == 5:
#                     # Bounding box format
#                     class_id = int(parts[0])
#                     x_center = float(parts[1])
#                     y_center = float(parts[2])
#                     width = float(parts[3])
#                     height = float(parts[4])
#
#                     image = drawing.draw_bounding_box(
#                         image, class_id, x_center, y_center, width, height
#                     )
#                 else:
#                     # Polygon segmentation format
#                     class_id = int(parts[0])
#                     coords = [float(coord) for coord in parts[1:]]
#
#                     image = drawing.draw_polygon(image, class_id, coords)
#
#             cv2.imshow(f"Annotated: {image_file}", image)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#
#         cv2.destroyAllWindows()
#
#     def remake(
#             self,
#             skip_empty: bool = True,
#             skip_healthy: bool = True,
#     ) -> None:
#         """
#         Remake the dataset by converting polygon annotations to bounding boxes.
#         This function will read the original dataset, convert polygon annotations
#         to bounding boxes, and save them in the remake directory.
#
#         Following steps are performed:
#         1. Create remake directory structure
#         2. For each mode (train, val, test):
#             for each image in the mode:
#                 read image and label
#                 if label is empty
#                     if name file contain "Healthy"
#                         skip (healthy class)
#                     else
#                         copy image and label to remake directory
#
#                 if label have class id is 2
#                     skip (healthy class)
#                 else
#                     if label is polygon format:
#                         convert polygon to bounding box
#                         save bounding box in remake directory
#                     else:
#                         copy image and label to remake directory
#
#         Note:
#         - The remake directory will be created if it does not exist.
#         - Class id 2 is considered as "Healthy" class and will be skipped.
#         - When label copy to remake directory, it will be decreased by 1 if class id is greater than 2.
#         """
#         print(
#             "================================== REMAKING DATASET =================================="
#         )
#
#         # if remake_directory exists, remove it
#         # self.reset_directory(self.remake_directory)
#
#         count_skipped = 0
#         for mode in DatasetMode:
#             images_path = os.path.join(self.dataset_directory, mode.value, "images")
#             labels_path = os.path.join(self.dataset_directory, mode.value, "labels")
#
#             remake_images_path = os.path.join(
#                 self.remake_directory, mode.value, "images"
#             )
#             remake_labels_path = os.path.join(
#                 self.remake_directory, mode.value, "labels"
#             )
#
#             os.makedirs(remake_images_path, exist_ok=True)
#             os.makedirs(remake_labels_path, exist_ok=True)
#
#             image_files = os.listdir(images_path)
#             label_files = os.listdir(labels_path)
#
#             for image_file in image_files:
#                 label_file = image_file.replace(".jpg", ".txt")
#                 if label_file not in label_files:
#                     print(
#                         f"Warning: No label found for image '{image_file}'. Skipping."
#                     )
#                     count_skipped += 1
#                     continue
#
#                 # read image
#                 image_path = os.path.join(images_path, image_file)
#                 copy_image = cv2.imread(image_path)
#                 if copy_image is None:
#                     print(f"Error reading image '{image_file}'. Skipping.")
#                     count_skipped += 1
#                     continue
#
#                 # read label
#                 label_path = os.path.join(labels_path, label_file)
#                 with open(label_path, "r") as file:
#                     labels = file.readlines()
#
#                 if not labels:
#                     if image_file.lower().startswith("healthy"):
#                         print(
#                             f"Skipping healthy image '{image_file}' with empty label."
#                         )
#                         count_skipped += 1
#                         continue
#                     else:
#                         if skip_empty:
#                             print(f"Skipping image '{image_file}' with empty label.")
#                             count_skipped += 1
#                             continue
#
#                         # Copy image and label to remake directory
#                         cv2.imwrite(
#                             os.path.join(remake_images_path, image_file), copy_image
#                         )
#                         with open(
#                                 os.path.join(remake_labels_path, label_file), "w"
#                         ) as f:
#                             f.write("")
#                         print(
#                             f"Copied empty label for image '{image_file}' to remake directory."
#                         )
#                         continue
#                 else:
#                     if image_file.lower().startswith("healthy"):
#                         print(
#                             f"Skipping healthy image '{image_file}' with non-empty label."
#                         )
#                         count_skipped += 1
#                         continue
#
#                     with open(os.path.join(remake_labels_path, label_file), "w") as f:
#                         for label in labels:
#                             parts = label.strip().split()
#                             class_id = int(parts[0])
#
#                             if class_id == 2:
#                                 # noinspection PyTypeChecker
#                                 print(
#                                     f"Skipping healthy class '{self.original_class_names[class_id]}' for image '{image_file}'."
#                                 )
#                                 count_skipped += 1
#                                 continue
#                             elif len(parts) < 5:
#                                 print(
#                                     f"Warning: label file '{label_file}' has invalid format. Skipping."
#                                 )
#                                 count_skipped += 1
#                                 continue
#                             elif len(parts) == 5:
#                                 # Bounding box format
#                                 x_center = float(parts[1])
#                                 y_center = float(parts[2])
#                                 width = float(parts[3])
#                                 height = float(parts[4])
#
#                                 # Write bounding box to remake label file
#                                 new_class_id = (
#                                     class_id - 1 if class_id > 2 else class_id
#                                 )
#                                 f.write(
#                                     f"{new_class_id} {x_center} {y_center} {width} {height}\n"
#                                 )
#                                 print(
#                                     f"Copied label with bbox format for image '{image_file}' to remake directory."
#                                 )
#                             else:
#                                 # Polygon format
#                                 coord = [float(coord) for coord in parts[1:]]
#                                 x_center, y_center, width, height = (
#                                     self.convert_polygon_to_bbox(
#                                         copy_image,
#                                         np.array(coord),
#                                     )
#                                 )
#
#                                 # Write bounding box to remake label file
#                                 new_class_id = (
#                                     class_id - 1 if class_id > 2 else class_id
#                                 )
#                                 f.write(
#                                     f"{new_class_id} {x_center} {y_center} {width} {height}\n"
#                                 )
#                                 print(
#                                     f"Copied label with polygon format for image '{image_file}' to remake directory."
#                                 )
#
#                     # Save the image in the remake directory
#                     cv2.imwrite(
#                         os.path.join(remake_images_path, image_file), copy_image
#                     )
#
#         print(
#             "======================================================================================"
#         )
#         print("Remake completed successfully! 🎉")
#         print(
#             "Dataset has been converted to bounding boxes and saved in the remake directory."
#         )
#         print(f"Please check directory {self.remake_directory}")
#         print(f"Total skipped images: {count_skipped}")
#         print(
#             "======================================================================================"
#         )
