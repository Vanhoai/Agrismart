from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from enum import Enum

from core.configuration import Configuration


class CollectionName(str, Enum):
    ACCOUNTS = "accounts"
    ROLES = "roles"
    SUBMISSIONS = "submissions"
    POSTS = "posts"


class Database:
    def __init__(self, config: Configuration):
        self.client = AsyncMongoClient(config.URI)
        self.db = self.client.agrismart  # name of the database

    def ping(self):
        return self.client.admin.command("ping")

    def collections(self):
        return self.db.list_collection_names()

    def get_collection(self, name: CollectionName) -> AsyncCollection:
        collection = self.db[name.value]
        return collection
