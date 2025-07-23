import os
from .account import AccountAugmenter

from core.database import Database, CollectionName


class Augmenter:
    def __init__(self, directory: str, database: Database) -> None:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")

        account_csv = os.path.join(directory, "accounts.csv")
        account_collection = database.get_collection(CollectionName.ACCOUNTS)
        self.account_augmenter = AccountAugmenter(account_csv, account_collection)

    async def monitor(self):
        await self.account_augmenter.monitor()


__all__ = ["Augmenter"]
