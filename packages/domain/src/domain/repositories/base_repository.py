from typing import Generic, Type, TypeVar

from domain.entities.base_entity import BaseEntity
from pymongo.asynchronous.collection import AsyncCollection

T = TypeVar("T", bound=BaseEntity)

class BaseRepository(Generic[T]):
    def __init__(self, collection: AsyncCollection, model: Type[T]):
        self.collection = collection
        self.model = model
