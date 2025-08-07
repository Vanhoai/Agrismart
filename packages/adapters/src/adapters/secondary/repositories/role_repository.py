from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import RoleEntity
from domain.repositories import IRoleRepository
from adapters.secondary.repositories import BaseRepository


class RoleRepository(BaseRepository[RoleEntity], IRoleRepository):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, RoleEntity)
