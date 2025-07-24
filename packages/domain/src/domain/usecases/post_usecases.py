from typing import List
from fastapi_camelcase import CamelModel
from abc import ABC, abstractmethod

from domain.entities import PostEntity


class CreatePostRequest(CamelModel):
    title: str
    image_url: str
    tags: List[str]
    captions: List[str]


class ManagePostUseCase(ABC):
    @abstractmethod
    async def create_post(self, account_id: str, req: CreatePostRequest) -> PostEntity: ...
