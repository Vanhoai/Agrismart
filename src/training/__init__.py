import os
import supervision as sv
from ultralytics import YOLO, SAM
import cv2
import numpy as np
import torch
import torchvision
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
from torch.export import export
import torchvision.models.detection as detection

from vision import AgrismartDataset

root_directory = os.getcwd()
dataset_directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")
yaml_path = os.path.join(dataset_directory, "data.yaml")

class_names = ['Bacterial Leaf Blight', 'Brown Spot', 'Healthy', 'Leaf Blast', 'Leaf Blight', 'Leaf Scald', 'Leaf Smut',
               'Narrow Brown Spot']


# def statistics(mode: str) -> None:
#     mode_image = os.path.join(dataset_directory, mode, "images")
#     mode_labels = os.path.join(dataset_directory, mode, "labels")
#
#     if not os.path.exists(mode_image) or not os.path.exists(mode_labels):
#         raise FileNotFoundError(f"Dataset directory for mode '{mode}' does not exist.")
#
#     # check image mapping with labels
#     image_files = os.listdir(mode_image)
#     label_files = os.listdir(mode_labels)
#
#     if len(image_files) != len(label_files):
#         print(f"Warning: Number of images ({len(image_files)}) does not match number of labels ({len(label_files)}).")
#
#     count = 0
#     for image_file in image_files:
#         # Check if there is a corresponding label file
#         label_file = image_file.replace(".jpg", ".txt")
#         if label_file not in label_files:
#             print(f"Warning: No label found for image '{image_file}'")
#         else:
#             count += 1
#
#     if count != len(image_files):
#         print(f"Warning: {len(image_files) - count} images do not have corresponding labels.")
#
#     print(f"Statistics for mode '{mode}':")
#     print(f"Total images: {len(image_files)}")
#     print(f"Total labels: {len(label_files)}")
#     print(f"Total valid images: {count}")
#
# class_colors = {
#     0: (0, 255, 0),    # Green
#     1: (0, 165, 255),  # Orange
#     2: (0, 0, 255),    # Red
#     3: (255, 0, 0),    # Blue
#     4: (255, 255, 0)   # Cyan
# }
#
# def draw_bounding_box(image, class_id, x_center, y_center, width, height):
#     h, w = image.shape[:2]
#
#     # Convert normalized coordinates to pixel coordinates
#     x_center_px = int(x_center * w)
#     y_center_px = int(y_center * h)
#     width_px = int(width * w)
#     height_px = int(height * h)
#
#     # Calculate top-left corner
#     x1 = int(x_center_px - width_px / 2)
#     y1 = int(y_center_px - height_px / 2)
#     x2 = int(x_center_px + width_px / 2)
#     y2 = int(y_center_px + height_px / 2)
#
#     # Get color for this class
#     color = class_colors.get(class_id, (255, 255, 255))
#
#     # Draw rectangle
#     cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
#
#     # Draw class label
#     class_name = class_names[class_id]
#     cv2.putText(image, class_name, (x1, y1 - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#
#     return image
#
# def draw_polygon(image, class_id, coords):
#     """Draw polygon for segmentation format"""
#     h, w = image.shape[:2]
#
#     # Convert normalized coordinates to pixel coordinates
#     points = []
#     for i in range(0, len(coords), 2):
#         x_px = int(coords[i] * w)
#         y_px = int(coords[i + 1] * h)
#         points.append([x_px, y_px])
#
#     # Convert to numpy array
#     points = np.array(points, dtype=np.int32)
#
#     # Get color for this class
#     color = class_colors.get(class_id, (255, 255, 255))
#
#     # Draw filled polygon with transparency
#     overlay = image.copy()
#     cv2.fillPoly(overlay, [points], color)
#     image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
#
#     # Draw polygon outline
#     cv2.polylines(image, [points], True, color, 2)
#
#     # Draw class label at centroid
#     M = cv2.moments(points)
#     if M["m00"] != 0:
#         cx = int(M["m10"] / M["m00"])
#         cy = int(M["m01"] / M["m00"])
#         class_name = class_names[class_id]
#         cv2.putText(image, class_name, (cx - 20, cy),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#
#     return image
#
# def show_sample_images(mode: str) -> None:
#     mode_image = os.path.join(dataset_directory, mode, "images")
#     mode_labels = os.path.join(dataset_directory, mode, "labels")
#
#     if not os.path.exists(mode_image) or not os.path.exists(mode_labels):
#         raise FileNotFoundError(f"Dataset directory for mode '{mode}' does not exist.")
#
#     image_files = os.listdir(mode_image)
#     label_files = os.listdir(mode_labels)
#
#     if len(image_files) == 0:
#         print(f"No images found in '{mode_image}'.")
#         return
#
#     for image_file in image_files[:10]:
#         label_processing = image_file.replace(".jpg", ".txt")
#         if label_processing not in label_files:
#             print(f"No label found for image '{image_file}'. Skipping.")
#             continue
#
#         # Read labels
#         label_path = os.path.join(mode_labels, label_processing)
#         with open(label_path, "r") as file:
#             labels = file.readlines()
#
#         # Read image
#         image_path = os.path.join(mode_image, image_file)
#         image = cv2.imread(image_path)
#
#         if image is None:
#             print(f"Error reading image '{image_file}'. Skipping.")
#             continue
#
#         print(f"Processing image: {image_file}")
#
#         # Process each label
#         for label in labels:
#             parts = label.strip().split()
#             if len(parts) < 5:
#                 continue
#
#             if len(parts) == 5:
#                 # Bounding box format
#                 class_id = int(parts[0])
#                 x_center = float(parts[1])
#                 y_center = float(parts[2])
#                 width = float(parts[3])
#                 height = float(parts[4])
#
#                 image = draw_bounding_box(image, class_id, x_center, y_center, width, height)
#
#             else:
#                 # Polygon segmentation format
#                 class_id = int(parts[0])
#                 coords = [float(coord) for coord in parts[1:]]
#
#                 image = draw_polygon(image, class_id, coords)
#
#         # Display image
#         cv2.imshow(f"Annotated: {image_file}", image)
#
#         # Save annotated image (optional)
#         output_path = f"annotated_{image_file}"
#         cv2.imwrite(output_path, image)
#         print(f"Saved annotated image: {output_path}")
#
#         # Wait for key press (press any key to continue, 'q' to quit)
#         key = cv2.waitKey(0)
#         if key == ord('q'):
#             break
#
#         cv2.destroyAllWindows()
#
#     cv2.destroyAllWindows()

def main() -> None:
    # Load dataset draw bounding boxes and show images
    # statistics("train")
    directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")
    dataset = AgrismartDataset(directory)
    print(dataset)

    # predict
    # model = YOLO("best.pt")
    # model.to("mps")
    # model.eval()

    # image_path = os.path.join(dataset_directory, "train", "images", "blast_orig_063_JPG_jpg.rf.9c4e34772d294448dd62a1ad6af17bfb.jpg")
    # image = cv2.imread(image_path)

    # cv2.imshow("Prediction", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # results = model.predict(source=image, save=True)
    # image = results[0].plot()
    # cv2.imshow("Prediction", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
