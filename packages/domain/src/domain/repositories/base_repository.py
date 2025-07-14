from typing import Generic, Type, TypeVar
from pymongo.asynchronous.collection import AsyncCollection

from domain.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)

class BaseRepository(Generic[T]):
    def __init__(self, collection: AsyncCollection, model: Type[T]):
        self.collection = collection
        self.model = model

    async def create(self, model: T):
        document = model.model_dump(exclude={"id"}, exclude_unset=True)
        result = await self.collection.insert_one(document)
        model.id = str(result.inserted_id)
        return model
