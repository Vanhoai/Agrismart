import asyncio
import os
from bson import ObjectId
from domain.entities.base_entity import BaseEntity
from loguru import logger
from typing import List, Optional, TypeVar, Generic
from pymongo.asynchronous.collection import AsyncCollection
from core.database import CollectionName
from abc import ABC, abstractmethod

T = TypeVar("T", bound="BaseEntity")


class Augmentation(Generic[T], ABC):
    NUM_COLLECTION_REQUIRED = {
        CollectionName.ACCOUNTS: 1000,
        CollectionName.ROLES: 10,
        CollectionName.SUBMISSIONS: 100,
        CollectionName.POSTS: 1000,
        CollectionName.DISEASES: 50,
        CollectionName.NOTIFICATIONS: 500,
    }

    def __init__(
        self,
        collection: AsyncCollection,
        collection_name: CollectionName,
    ) -> None:
        self.collection = collection
        self.collection_name = collection_name

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(exclude_unset=True)

        # convert all fields contain "_id" string to ObjectId
        for key, value in entity_dict.items():
            if "_id" in key and key != "_id":
                entity_dict[key] = ObjectId(value)

        result = await self.collection.insert_one(entity_dict)
        entity.id = str(result.inserted_id)
        return entity

    async def monitor(self) -> None:
        num_required = self.NUM_COLLECTION_REQUIRED.get(self.collection_name, 0)
        num_documents = await self.collection.count_documents({})

        if num_documents >= num_required:
            logger.info(f"Already have {num_documents} documents in {self.collection_name}, no need to augment ✅")
            return

        logger.info(f"Number of documents in {self.collection_name}: {num_documents}, augmenting...")
        start_time = asyncio.get_event_loop().time()

        # Make sure we don't exceed the required number
        count = 0

        entities = []
        with open(self.csv, "r") as file:
            data = file.readlines()

            # noinspection PyTypeChecker
            for i in range(len(data)):
                if i == 0:
                    continue

                if num_documents + count >= num_required:
                    logger.info(f"Reached required number of documents: {num_required}, stopping augmentation.")
                    break

                line = data[i].strip()

                parts = self.process_line(line)
                entities.append(parts)
                count += 1

        logger.info(f"Number of entities to insert: {len(entities)}")
        tasks = []
        for entity in entities:
            tasks.append(self.insert_one(entity))

        results = await asyncio.gather(*tasks)
        for result in results:
            if result is None:
                continue

            logger.info(f"Inserted entity: {result}")

        end_time = asyncio.get_event_loop().time()
        logger.info(f"Time taken to insert entities: {end_time - start_time:.2f} seconds")

    @abstractmethod
    async def insert_one(self, attrs=None) -> Optional[T]: ...

    @abstractmethod
    def process_line(self, line: str) -> List[str]: ...
