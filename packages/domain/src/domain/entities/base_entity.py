from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from core.helpers import TimeHelper


class BaseEntity(CamelModel):
    id: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def __init__(self):
        super().__init__()
        self.id = None
        self.created_at = TimeHelper.vn_timezone()
        self.updated_at = TimeHelper.vn_timezone()
        self.deleted_at = None
