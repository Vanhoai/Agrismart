import os
import asyncio
from pymongo.asynchronous.collection import AsyncCollection
from domain.entities import AccountEntity


class AccountAugmenter:
    NUM_REQUIRED_ACCOUNTS = 1000

    def __init__(self, csv: str, collection: AsyncCollection) -> None:
        if not os.path.exists(csv):
            raise FileNotFoundError(f"CSV file {csv} does not exist.")
        self.csv = csv
        self.collection = collection

    async def monitor(self):
        """
        Monitor the account by reading the CSV file.
        This method should implement the logic to read and process the CSV file.
        """
        num_accounts = await self.collection.count_documents({})
        if num_accounts >= self.NUM_REQUIRED_ACCOUNTS:
            print(f"Num account already reached: {num_accounts}, no need to augment.")
            return

        accounts = []
        with open(self.csv, "r") as file:
            data = file.readlines()
            for line in data:
                parts = line.strip().split(",")
                [username, email, avatar] = parts
                if username == "username" or email == "email" or avatar == "avatar":
                    print("Skipping header line.")
                    continue

                accounts.append((username, email, avatar))

        print(f"Number of accounts to insert: {len(accounts)}")
        start_time = asyncio.get_event_loop().time()
        tasks = []
        for username, email, avatar in accounts:
            tasks.append(self.insert(username, email, avatar))

        entities = await asyncio.gather(*tasks)
        for entity in entities:
            print(f"Inserted account: {entity.username} with ID: {entity._id}")

        end_time = asyncio.get_event_loop().time()
        print(f"Time taken to insert accounts: {end_time - start_time:.2f} seconds")
        # Time taken to insert accounts: 31.92 seconds

    async def insert(self, username: str, email: str, avatar: str) -> AccountEntity:
        device_token = "bGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3MzE0MzU2NjE0ODctbX"
        entity = AccountEntity.create(
            username=username,
            email=email,
            avatar=avatar,
            device_token=device_token,
        )

        entity_dict = entity.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(entity_dict)
        entity._id = str(result.inserted_id)
        return entity
