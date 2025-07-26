from typing import List, Optional
from pymongo.asynchronous.collection import AsyncCollection
from domain.entities import AccountEntity
from core.database import CollectionName

from .base import Augmentation


class AccountAugmenter(Augmentation[AccountEntity]):
    def __init__(
        self,
        csv: str,
        collection: AsyncCollection,
        collection_name: CollectionName,
    ) -> None:
        super().__init__(csv, collection, collection_name)

    async def insert_one(self, attrs=None) -> Optional[AccountEntity]:
        if attrs is None:
            attrs = []

        [username, email, avatar] = attrs
        device_token = "bGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3MzE0MzU2NjE0ODctbX"
        entity = AccountEntity.create(
            username=username,
            email=email,
            avatar=avatar,
            device_token=device_token,
        )

        entity_dict = entity.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(entity_dict)
        entity.id = str(result.inserted_id)
        return entity

    def process_line(self, line: str) -> List[str]:
        return line.strip().split(",")
