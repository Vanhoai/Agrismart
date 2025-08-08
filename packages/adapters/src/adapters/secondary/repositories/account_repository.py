from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import AccountEntity
from domain.repositories import IAccountRepository

from .base_repository import BaseRepository


class AccountRepository(BaseRepository[AccountEntity], IAccountRepository):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, AccountEntity)
