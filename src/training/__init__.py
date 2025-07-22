import os
from ultralytics import YOLO
from vision.constants import VisionConstants


def main() -> None:
    yaml_path = os.path.join(VisionConstants.REMAKE_DIRECTORY, "data.yaml")
    model = YOLO("yolo11n.pt")
    results = model.train(data=yaml_path, epochs=100)
    print(results)
