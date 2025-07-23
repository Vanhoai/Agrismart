from bson import ObjectId
from typing import Generic, Type, TypeVar, Optional, List, Tuple, Literal
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    def __init__(self, collection: AsyncCollection, model: Type[T]):
        self.collection = collection
        self.model = model

    def convert_doc_to_entity(self, doc: dict) -> T:
        doc["_id"] = str(doc["_id"])

        # convert all fields contain "_id" from ObjectId to string
        for key, value in doc.items():
            if "_id" in key and key != "_id":
                doc[key] = str(value) if isinstance(value, ObjectId) else value

        return self.model(**doc)

    async def find_one(self, query: dict) -> Optional[T]:
        entity_dict = await self.collection.find_one(query)
        if entity_dict:
            return self.convert_doc_to_entity(entity_dict)

        return None

    async def find(self, query: dict = {}) -> list[T]:
        cursor = self.collection.find(query)
        docs = await cursor.to_list(length=None)
        return [self.convert_doc_to_entity(doc) for doc in docs]

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(exclude_unset=True)

        # convert all fields contain "_id" string to ObjectId
        for key, value in entity_dict.items():
            if "_id" in key and key != "_id":
                entity_dict[key] = ObjectId(value)

        result = await self.collection.insert_one(entity_dict)
        entity.id = str(result.inserted_id)
        return entity

    async def paginated(
        self,
        query: dict = {},
        skip: int = 0,
        limit: int = 10,
        order: str = "asc",
        order_by: str = "created_at",
    ) -> Tuple[List[T], int]:
        cursor = self.collection.find(query).skip(skip).limit(limit).sort(order_by, ASCENDING if order == "asc" else DESCENDING)
        docs = await cursor.to_list(length=None)
        total = await self.collection.count_documents(query)
        return [self.convert_doc_to_entity(doc) for doc in docs], total
