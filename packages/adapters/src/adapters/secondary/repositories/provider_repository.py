from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import ProviderEntity
from domain.repositories import IProviderRepository
from .base_repository import BaseRepository


class ProviderRepository(BaseRepository[ProviderEntity], IProviderRepository):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, ProviderEntity)
