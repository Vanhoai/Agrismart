from typing import List

from core.helpers import TimeHelper
from domain.entities import BaseEntity


class PostEntity(BaseEntity):
    account_id: str
    image_url: str
    title: str
    caption: List[str]
    tags: List[str]
    viewer: int
    favorite: int

    @staticmethod
    def create(
        account_id: str,
        image_url: str,
        title: str,
        caption: List[str],
        tags: List[str],
    ) -> "PostEntity":
        return PostEntity(
            _id=None,
            account_id=account_id,
            image_url=image_url,
            title=title,
            caption=caption,
            tags=tags,
            viewer=0,
            favorite=0,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
