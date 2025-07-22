from typing import Generic, Type, TypeVar
from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    def __init__(self, collection: AsyncCollection, model: Type[T]):
        self.collection = collection
        self.model = model
