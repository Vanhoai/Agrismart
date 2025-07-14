from ultralytics import YOLO

source = "/Users/hinsun/Workspace/Software/Agrismart/assets/traffic.mp4"

def main() -> None:
    # Load a pretrained YOLO model (recommended for training)
    model = YOLO("yolo11n.pt")
    results = model.track(source=source, show=True)
