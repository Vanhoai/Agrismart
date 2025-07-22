from typing import List

from domain.entities import BaseEntity


class PostEntity(BaseEntity):
    account_id: str
    image_url: str
    caption: str
    tags: List[str]
    viewer: int
    favorite: int


def __init__(self, account_id: str, image_url: str, caption: str, tags: List[str], viewer: int, favorite: int):
    super().__init__()
    self.account_id = account_id
    self.image_url = image_url
    self.caption = caption
    self.tags = tags
    self.viewer = viewer
    self.favorite = favorite
    