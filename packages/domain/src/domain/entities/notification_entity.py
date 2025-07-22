from enum import Enum

from domain.entities import BaseEntity


class NotificationType(Enum):
    SUBMISSION = "submission"
    DISEASE = "disease"


class NotificationEntity(BaseEntity):
    account_id: str
    ref_id: str
    ref_type: str
    content: str


def __init__(self, account_id: str, ref_id: str, ref_type: NotificationType, content: str):
    super().__init__()
    self.account_id = account_id
    self.ref_id = ref_id
    self.type = ref_type.value
    self.content = content
