import cv2
import os
from typing import List
from insightface.app import FaceAnalysis

from .models import FaceDetected


class FaceDetector:
    def __init__(self) -> None:
        self.app = FaceAnalysis(
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
            allowed_modules=["detection", "recognition"],
        )

        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def detect(self, image_path: str) -> List[FaceDetected]:
        if not os.path.exists(image_path):
            raise FileNotFoundError("Path to the image not found 🥺")

        image = cv2.imread(image_path)
        faces = self.app.get(image)
        if not faces:
            print("No faces detected")
            return []

        return [FaceDetected.from_dict(face) for face in faces]
