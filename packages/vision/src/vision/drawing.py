import cv2
import os
import numpy as np

class Drawing:
    def __init__(self, class_names):
        self.class_names = class_names
        self.class_colors = {
            0: (0, 255, 0),    # Green
            1: (0, 165, 255),  # Orange
            2: (0, 0, 255),    # Red
            3: (255, 0, 0),    # Blue
            4: (255, 255, 0)   # Cyan
        }

    def draw_bounding_box(self, image, class_id, x_center, y_center, width, height):
        h, w = image.shape[:2]

        # Convert normalized coordinates to pixel coordinates
        x_center_px = int(x_center * w)
        y_center_px = int(y_center * h)
        width_px = int(width * w)
        height_px = int(height * h)

        # Calculate top-left corner
        x1 = int(x_center_px - width_px / 2)
        y1 = int(y_center_px - height_px / 2)
        x2 = int(x_center_px + width_px / 2)
        y2 = int(y_center_px + height_px / 2)

        # Get color for this class
        color = self.class_colors.get(class_id, (255, 255, 255))

        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Draw class label
        class_name = self.class_names[class_id]
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return image
    
    def draw_polygon(self, image, class_id, coords):
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
        color = self.class_colors.get(class_id, (255, 255, 255))

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
            class_name = self.class_names[class_id]
            cv2.putText(image, class_name, (cx - 20, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return image