from domain.entities import BaseEntity
from core.helpers import TimeHelper


class SubmissionEntity(BaseEntity):
    account_id: str
    disease_id: str
    image_url: str
    confidence: float

    @staticmethod
    def create(
        account_id: str,
        disease_id: str,
        image_url: str,
        confidence: float = 0.0,
    ) -> "SubmissionEntity":
        return SubmissionEntity(
            _id=None,
            account_id=account_id,
            disease_id=disease_id,
            image_url=image_url,
            confidence=confidence,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
