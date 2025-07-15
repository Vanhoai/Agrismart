import supervision as sv
from ultralytics import YOLO, SAM
import cv2

# source_path = "/Users/hinsun/Workspace/Software/Agrismart/assets/traffic.mp4"
image_path = "/Users/hinsun/Workspace/Software/Agrismart/assets/traffic.jpg"

def main() -> None:
    # (2160, 3840, 3)
    # model = YOLO("yolo11x.pt")

    # model.info()
    # model.predict(source=image_path, imgsz=3840, conf=0.25, show=True, save=True)

    model = SAM("sam2.1_b.pt")
    results = model(image_path, points=[[992, 1630], [1379, 1325], [1397, 1200], [1450, 1024], [1334, 883], [1118, 667], [1055, 707], [844, 634], [725, 601], [1015, 558], [401, 498], [826, 533]])
    image = results[0].plot(labels=False)
    cv2.imshow("SAM", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
