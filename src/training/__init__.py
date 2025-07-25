import os
from ultralytics import YOLO
from vision.constants import VisionConstants


def main() -> None:
    best_model_path = VisionConstants.BEST_MODEL_PATH
    model = YOLO(best_model_path)

    REMAKE_IMAGES = os.path.join(VisionConstants.REMAKE_DIRECTORY, "test", "images")

    # Get 10 images sample in the remake directory
    images = os.listdir(REMAKE_IMAGES)[:10]
    images = [os.path.join(REMAKE_IMAGES, image) for image in images]

    results = model.predict(source=images, save=True, save_txt=True)
    print(results)

    # yaml_path = os.path.join(VisionConstants.REMAKE_DIRECTORY, "data.yaml")
    # results = model.train(data=yaml_path, epochs=100)
