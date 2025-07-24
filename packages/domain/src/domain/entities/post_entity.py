from typing import List

from core.helpers import TimeHelper
from domain.entities import BaseEntity


class PostEntity(BaseEntity):
    account_id: str
    image_url: str
    title: str
    captions: List[str]
    tags: List[str]
    viewer: int
    favorite: int

    @staticmethod
    def create(
        account_id: str,
        image_url: str,
        title: str,
        captions: List[str],
        tags: List[str],
    ) -> "PostEntity":
        return PostEntity(
            account_id=account_id,
            image_url=image_url,
            title=title,
            captions=captions,
            tags=tags,
            viewer=0,
            favorite=0,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
