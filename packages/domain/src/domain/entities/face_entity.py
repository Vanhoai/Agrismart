from dataclasses import dataclass
from typing import List
from numpy.typing import NDArray
from enum import Enum
from fastapi_camelcase import CamelModel

from .base_entity import BaseEntity
from core.helpers import TimeHelper

MIN_EMBEDDINGS_REQUIRED = 3
MAX_EMBEDDINGS_ALLOWED = 10


class FacePose(Enum):
    FRONTAL = "frontal"
    LEFT_PROFILE = "left_profile"
    RIGHT_PROFILE = "right_profile"
    UPWARD = "upward"
    DOWNWARD = "downward"


class EnrollmentStatus(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    VERIFIED = "verified"


@dataclass
class FaceEmbedding(CamelModel):
    embedding: NDArray
    confidence_score: float
    pose_type: FacePose
    quantity_score: float
    created_at: str


class FaceEntity(BaseEntity):
    account_id: str
    embeddings: List[FaceEmbedding]
    enrollment_status: EnrollmentStatus = EnrollmentStatus.INCOMPLETE

    @staticmethod
    def create(
        account_id: str,
        embeddings: List[FaceEmbedding],
        enrollment_status: EnrollmentStatus = EnrollmentStatus.INCOMPLETE,
    ) -> "FaceEntity":
        return FaceEntity(
            account_id=account_id,
            embeddings=embeddings,
            enrollment_status=enrollment_status,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
