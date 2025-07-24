from domain.entities import PostEntity
from domain.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository[PostEntity]):
    def __init__(self, collection):
        super().__init__(collection, PostEntity)
