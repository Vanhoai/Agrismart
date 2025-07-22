from typing import List

from core.helpers import TimeHelper
from domain.entities import BaseEntity


class PostEntity(BaseEntity):
    account_id: str
    image_url: str
    caption: str
    tags: List[str]
    viewer: int
    favorite: int

    @staticmethod
    def create(
        account_id: str,
        image_url: str,
        caption: str,
        tags: List[str],
        viewer: int = 0,
        favorite: int = 0,
    ) -> "PostEntity":
        return PostEntity(
            _id=None,
            account_id=account_id,
            image_url=image_url,
            caption=caption,
            tags=tags,
            viewer=viewer,
            favorite=favorite,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
