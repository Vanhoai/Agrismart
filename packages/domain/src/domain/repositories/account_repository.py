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
        print(f"Creating account with data: {entity_dict}")

        result = await self.collection.insert_one(entity_dict)
        print(f"Insert result: {result}")

        entity._id = str(result.inserted_id)

        print(f"Account created with ID: {entity._id}")
        print(f"Account entity: {entity}")
        return entity
