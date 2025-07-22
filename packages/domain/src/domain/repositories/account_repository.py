from typing import Optional
from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import AccountEntity
from domain.repositories.base_repository import BaseRepository


class AccountRepository(BaseRepository[AccountEntity]):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, AccountEntity)

    async def find_by_email(self, email: str) -> Optional[AccountEntity]:
        entity_dict = await self.collection.find_one({"email": email})
        if entity_dict:
            return self.model(**entity_dict)

        return None

    async def create(self, entity: AccountEntity) -> AccountEntity:
        entity_dict = entity.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(entity_dict)
        entity._id = str(result.inserted_id)
        return entity

    async def find_accounts(self):
        query = self.collection.find().skip(0).limit(10)
        docs = await query.to_list()
        records = await self.collection.count_documents({})
        return docs, records
