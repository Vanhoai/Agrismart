from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from core.helpers import TimeHelper


class BaseEntity(CamelModel):
    _id: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
