from bson import ObjectId
from typing import Generic, Type, TypeVar, Optional, List, Tuple, Literal
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.collection import AsyncCollection

from core.base import Meta
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

    async def find(self, query=None) -> list[T]:
        if query is None:
            query = {}

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
        query=None,
        page: int = 1,
        page_size: int = 20,
        order: str = "asc",
        order_by: str = "created_at",
    ) -> Tuple[List[T], Meta]:
        if query is None:
            query = {}

        skip = (page - 1) * page_size
        limit = page_size

        cursor = (
            self.collection.find(query)
            .skip(skip)
            .limit(limit)
            .sort(order_by, ASCENDING if order == "asc" else DESCENDING)
        )

        docs = await cursor.to_list(length=None)
        total = await self.collection.count_documents(query)

        total_page = (total // page_size) + (1 if total % page_size > 0 else 0)

        meta = Meta(
            page=page,
            page_size=page_size,
            total_record=total,
            total_page=total_page,
        )

        return [self.convert_doc_to_entity(doc) for doc in docs], meta
