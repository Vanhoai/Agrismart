from domain.entities import RoleEntity
from domain.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[RoleEntity]):
    def __init__(self, collection):
        super().__init__(collection, RoleEntity)
