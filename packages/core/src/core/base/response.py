from typing import Any
from fastapi_camelcase import CamelModel

PAGE = 1
PAGE_SIZE = 30

class HttpResponse(CamelModel):
    status_code: int
    message: str
    data: Any = None

class Meta(CamelModel):
    page: int
    page_size: int
    total_page: int
    total_record: int

    @staticmethod
    def empty():
        return Meta(page=PAGE, page_size=PAGE_SIZE, total_page=1, total_record=0)


class HttpPaginationResponse(CamelModel):
    status_code: int
    message: str
    meta: Meta
    data: Any = None
