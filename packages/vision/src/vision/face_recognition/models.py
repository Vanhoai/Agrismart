import numpy as np
from numpy.typing import NDArray


class FaceDetected:
    def __init__(
        self,
        det_score: float,
        kps: NDArray[np.float64],
        bbox: NDArray[np.float64],
        embedding: NDArray[np.float64],
    ) -> None:
        self.__det_score = det_score
        self.__kps = kps
        self.__bbox = bbox
        self.__embedding = embedding

    @property
    def det_score(self) -> float:
        return self.__det_score

    @property
    def kps(self) -> NDArray[np.float64]:
        return self.__kps

    @property
    def bbox(self) -> NDArray[np.float64]:
        return self.__bbox

    @property
    def embedding(self) -> NDArray[np.float64]:
        return self.__embedding

    @staticmethod
    def from_dict(data: dict) -> "FaceDetected":
        return FaceDetected(
            det_score=data["det_score"],
            kps=np.array(data["kps"], dtype=np.float64),
            bbox=np.array(data["bbox"], dtype=np.float64),
            embedding=np.array(data["embedding"], dtype=np.float64),
        )
