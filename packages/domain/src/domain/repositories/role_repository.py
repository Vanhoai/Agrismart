from core import database, CollectionName

from domain.entities import RoleEntity
from domain.repositories.base_repository import BaseRepository

class RoleRepository(BaseRepository[RoleEntity]):
    def __init__(self):
        collection = database.get_collection(CollectionName.ROLES)
        super().__init__(collection, RoleEntity)
