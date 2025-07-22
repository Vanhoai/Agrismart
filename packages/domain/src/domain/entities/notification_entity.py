from enum import Enum

from core.helpers import TimeHelper
from domain.entities import BaseEntity


class NotificationType(Enum):
    SUBMISSION = "submission"
    DISEASE = "disease"


class NotificationEntity(BaseEntity):
    account_id: str
    ref_id: str
    ref_type: str
    content: str

    @staticmethod
    def create(
        account_id: str,
        ref_id: str,
        ref_type: NotificationType,
        content: str,
    ) -> "NotificationEntity":
        return NotificationEntity(
            _id=None,
            account_id=account_id,
            ref_id=ref_id,
            ref_type=ref_type.value,
            content=content,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
