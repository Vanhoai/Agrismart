import os
import cv2
import numpy as np
from typing import List

from .base_dataset import AgrismartBaseDataset, DatasetMode


# +-----------------------+-------+--------+----------+-------+
# |         Class         | Files | BBoxes | Polygons | Total |
# +-----------------------+-------+--------+----------+-------+
# | Bacterial Leaf Blight |  480  |  509   |    36    |  545  |
# |      Brown Spot       |  735  |  3735  |   625    | 4360  |
# |        Healthy        |  584  |   76   |   554    |  630  |
# |      Leaf Blast       |  782  |  1741  |   307    | 2048  |
# |      Leaf Blight      |  353  |  336   |   244    |  580  |
# |      Leaf Scald       |  403  |  131   |   353    |  484  |
# |       Leaf Smut       |  28   |   1    |   145    |  146  |
# |   Narrow Brown Spot   |  485  |  1285  |   828    | 2113  |
# +-----------------------+-------+--------+----------+-------+
# |       Total           | 3850  |  10184 |   3092   | 13276 |
# +-----------------------+-------+--------+----------+-------+
# remake ignore healthy images -> 3850 - 584 = 3266

class AgrismartRemakeDataset(AgrismartBaseDataset):
    def __init__(self, directory: str, classnames: List[str]) -> None:
        super().__init__(directory, classnames)

    def remake(self, original_directory: str) -> None:
        if not os.path.exists(original_directory):
            raise FileNotFoundError("Please provide a valid original directory.")

        self.reset_directory(self.directory)
        for mode in DatasetMode:
            images_path = os.path.join(original_directory, mode.value, "images")
            labels_path = os.path.join(original_directory, mode.value, "labels")

            remake_images_path = os.path.join(self.directory, mode.value, "images")
            remake_labels_path = os.path.join(self.directory, mode.value, "labels")

            os.makedirs(remake_images_path, exist_ok=True)
            os.makedirs(remake_labels_path, exist_ok=True)

            image_files = os.listdir(images_path)

            count_healthy = 0
            count_process = 0

            for image_file in image_files:
                label_file = image_file.replace(".jpg", ".txt")

                label_path = os.path.join(labels_path, label_file)
                with open(label_path, "r") as file:
                    labels = file.readlines()

                if not labels:  # ignore empty file
                    continue

                class_id = None
                bboxes = []

                image = cv2.imread(os.path.join(images_path, image_file))

                for label in labels:
                    parts = label.strip().split()
                    class_id = int(parts[0])

                    if len(parts) == 5:
                        # bounding box format
                        x_center, y_center, width, height = map(float, parts[1:])
                        bboxes.append((class_id, x_center, y_center, width, height))
                    else:
                        # polygon format
                        coordinates = [float(coord) for coord in parts[1:]]
                        x_center, y_center, width, height = (
                            self.convert_polygon_to_bbox(
                                image,
                                np.array(coordinates),
                            )
                        )
                        bboxes.append((class_id, x_center, y_center, width, height))

                if class_id == 2:
                    # skip healthy images
                    count_healthy += 1
                else:
                    # write image and labels to remake dataset
                    # note: decrease class id by 1 for class id greater than 2
                    count_process += 1
                    print(f"Remaking image {image_file} with labels: {bboxes}")

                    cv2.imwrite(os.path.join(remake_images_path, image_file), image)
                    with open(os.path.join(remake_labels_path, label_file), "w") as file:
                        for bbox in bboxes:
                            if bbox[0] > 2:
                                file.write(f"{bbox[0] - 1} {bbox[1]} {bbox[2]} {bbox[3]} {bbox[4]}\n")
                            else:
                                file.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]} {bbox[4]}\n")

            print(f"Processed {count_process} images.")
            print(f"Skipped {count_healthy} healthy images.")
