import os
from .account import AccountAugmenter
from .post import PostAugmenter

from core.database import Database, CollectionName


class Augmenter:
    def __init__(self, directory: str, database: Database) -> None:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")

        account_csv = os.path.join(directory, "accounts.csv")
        post_csv = os.path.join(directory, "posts.csv")

        self.account_collection = database.get_collection(CollectionName.ACCOUNTS)
        self.post_collection = database.get_collection(CollectionName.POSTS)

        self.account_augmenter = AccountAugmenter(account_csv, self.account_collection, CollectionName.ACCOUNTS)
        self.post_augmenter = PostAugmenter(post_csv, self.post_collection, CollectionName.POSTS)

    async def monitor(self):
        await self.account_augmenter.monitor()

        accounts = await self.account_collection.find({}).to_list(length=None)
        account_ids = [str(account["_id"]) for account in accounts]
        self.post_augmenter.provide_accounts(account_ids)
        await self.post_augmenter.monitor()


__all__ = ["Augmenter"]
