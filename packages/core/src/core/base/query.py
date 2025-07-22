from typing import Literal
from fastapi_camelcase import CamelModel
from pydantic import Field


class BaseQuery(CamelModel):
    page: int = Field(1, gt=0, le=50)
    page_size: int = Field(30, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    order: Literal["asc", "desc"] = "desc"
    search: str = ""
