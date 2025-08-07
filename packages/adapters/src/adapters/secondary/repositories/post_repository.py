from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import PostEntity
from domain.repositories import IPostRepository

from .base_repository import BaseRepository


class PostRepository(BaseRepository[PostEntity], IPostRepository):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, PostEntity)
