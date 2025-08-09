from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray


@dataclass
class FaceDetected:
    det_score: float
    kps: NDArray[np.float64]
    bbox: NDArray[np.float64]
    embedding: NDArray[np.float64]
    pose_type: str = "unknown"
    yaw: float = 0.0
    pitch: float = 0.0
    quality_score: float = 0.0

    @classmethod
    def from_dict(cls, face: dict) -> "FaceDetected":
        return FaceDetected(
            det_score=face.get("det_score", 0.0),
            kps=face.get("kps", np.array([])),
            bbox=face.get("bbox", np.array([])),
            embedding=face.get("embedding", np.array([])),
        )
