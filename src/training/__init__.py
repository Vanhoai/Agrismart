import os
import cv2
import numpy as np

root_path = os.getcwd()
image_path = os.path.join(root_path, "datasets", "rice-leaf-diseases", "val", "images",
                          "bacterial_leaf_blight-190-_JPG_jpg.rf.b1b836fd5c000bab6130e9d63a25c910.jpg")

label_path = os.path.join(root_path, "datasets", "rice-leaf-diseases", "val", "labels",
                          "bacterial_leaf_blight-190-_JPG_jpg.rf.b1b836fd5c000bab6130e9d63a25c910.txt")

class_colors = {
    0: (0, 255, 0),  # Green
    1: (0, 165, 255),  # Orange
    2: (0, 0, 255),  # Red
    3: (255, 0, 0),  # Blue
    4: (255, 255, 0)  # Cyan
}

class_names = [
    "Bacterial Leaf Blight",
    "Brown Spot",
    "Healthy",
    "Leaf Blast",
    "Leaf Blight",
    "Leaf Scald",
    "Leaf Smut",
    "Narrow Brown Spot"
]


def draw_bounding_box(image, class_id, x_center, y_center, width, height):
    h, w = image.shape[:2]

    # Convert normalized coordinates to pixel coordinates
    x_center_px = int(x_center * w)
    y_center_px = int(y_center * h)
    width_px = int(width * w)
    height_px = int(height * h)

    # Calculate top-left corner
    x1 = int(x_center_px - width_px / 2)
    y1 = int(y_center_px - height_px / 2)

    # Calculate bottom-right corner
    x2 = int(x_center_px + width_px / 2)
    y2 = int(y_center_px + height_px / 2)

    # Get color for this class
    color = class_colors.get(class_id, (255, 255, 255))

    # Draw rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    # Draw class label
    class_name = class_names[class_id]
    cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image


def draw_polygon(image, class_id, coords):
    h, w = image.shape[:2]

    # Convert normalized coordinates to pixel coordinates
    points = []
    for i in range(0, len(coords), 2):
        x_px = int(coords[i] * w)
        y_px = int(coords[i + 1] * h)
        points.append([x_px, y_px])

    # Convert to numpy array
    points = np.array(points, dtype=np.int32)

    # Get color for this class
    color = class_colors.get(class_id, (255, 255, 255))

    # Draw filled polygon with transparency
    overlay = image.copy()
    cv2.fillPoly(overlay, [points], color)
    image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

    # Draw polygon outline
    cv2.polylines(image, [points], True, color, 2)

    # Draw class label at centroid
    M = cv2.moments(points)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        class_name = class_names[class_id]
        cv2.putText(image, class_name, (cx - 20, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image


def main() -> None:
    image = cv2.imread(image_path)
    cv2.imshow("Original Image", image)

    with open(label_path, "r") as file:
        labels = file.readlines()

    for label in labels:
        parts = label.strip().split()
        class_id = int(parts[0])
        coord = [float(coord) for coord in parts[1:]]

        # convert to points - R(D, 2)
        h, w = image.shape[:2]

        # Convert normalized coordinates to pixel coordinates
        points = []
        for i in range(0, len(coord), 2):
            x_px = int(coord[i] * w)
            y_px = int(coord[i + 1] * h)
            points.append([x_px, y_px])

        points = np.array(points, dtype=np.int32)
        x_min, y_min = np.min(points, axis=0)
        x_max, y_max = np.max(points, axis=0)

        color = class_colors.get(class_id, (255, 255, 255))

        # Draw rectangle
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

        # Draw class label
        class_name = class_names[class_id]
        cv2.putText(image, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("BBoxes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Load dataset draw bounding boxes and show images
    # statistics("train")
    # directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")
    # dataset = AgrismartDataset(directory)
    # dataset.show_original_sample()

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
