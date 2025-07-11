from core import database, CollectionName

from domain.entities import AccountEntity
from domain.repositories.base_repository import BaseRepository

class AccountRepository(BaseRepository[AccountEntity]):
    def __init__(self):
        collection = database.get_collection(CollectionName.ACCOUNTS)
        super().__init__(collection, AccountEntity)
