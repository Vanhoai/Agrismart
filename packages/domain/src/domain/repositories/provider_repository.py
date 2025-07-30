from .base_repository import BaseRepository
from domain.entities import ProviderEntity

class ProviderRepository(BaseRepository[ProviderEntity]):
    def __init__(self, collection):
        super().__init__(collection, ProviderEntity)
