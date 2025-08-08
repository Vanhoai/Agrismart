from abc import ABC
from typing import Optional
from datetime import datetime
from typing import Optional
from pydantic import Field

from fastapi_camelcase import CamelModel


class BaseEntity(CamelModel, ABC):
    id: Optional[str] = Field(default=None, alias="id")
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
