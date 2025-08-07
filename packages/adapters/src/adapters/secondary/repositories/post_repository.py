from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import PostEntity
from domain.repositories import IPostRepository
from adapters.secondary.repositories import BaseRepository


class PostRepository(BaseRepository[PostEntity], IPostRepository):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, PostEntity)
