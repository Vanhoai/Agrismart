import os
import supervision as sv
from ultralytics import YOLO, SAM
import cv2

root_directory = os.getcwd()
dataset_directory = os.path.join(root_directory, "datasets", "rice-leaf-diseases")
yaml_path = os.path.join(dataset_directory, "data.yaml")

def main() -> None:
    model = YOLO("yolo11n.pt")
    results = model.train(data=yaml_path, epochs=100, imgsz=640, batch=1, device="mps")
