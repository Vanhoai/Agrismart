import cv2
import os
import numpy as np
from typing import Optional
from insightface.app import FaceAnalysis
from loguru import logger
from .models import FaceDetected


class FaceDetector:
    def __init__(self) -> None:
        self.app = FaceAnalysis(
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
            allowed_modules=["detection", "recognition"],
        )

        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def detect_from_path(self, image_path: str) -> Optional[FaceDetected]:
        if not os.path.exists(image_path):
            logger.error(f"Image path does not exist: {image_path}")
            return None

        image = cv2.imread(image_path)
        return self.detect_from_image(image)

    def detect_from_bytes(self, image_bytes: bytes) -> Optional[FaceDetected]:
        array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(array, cv2.IMREAD_COLOR)
        return self.detect_from_image(image)

    def detect_from_image(self, image: np.ndarray) -> Optional[FaceDetected]:
        if image is None or not isinstance(image, np.ndarray):
            logger.error(f"Image is None or not instance of np.ndarray 🥺")
            return None

        faces = self.app.get(image)
        if not faces:
            logger.warning("No faces detected in the image.")
            return None

        if len(faces) > 2:
            logger.warning(f"Multiple face detection not supported 😂, found {len(faces)} faces.")
            return None

        face = faces[0]
        # pose_type, yaw, pitch = self.pose_analyzer.analyze_pose(face)
        # quality_score = self.quality_analyzer.calculate_quality(image, face)
        face_detected = FaceDetected.from_dict(face)
        # update face_detected with additional attributes if needed
        return face_detected
