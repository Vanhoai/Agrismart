from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from pymongo.asynchronous.collection import AsyncCollection
from enum import Enum

from core.configuration import Configuration


class CollectionName(str, Enum):
    ACCOUNTS = "accounts"
    ROLES = "roles"
    SUBMISSIONS = "submissions"
    POSTS = "posts"
    DISEASES = "diseases"
    NOTIFICATIONS = "notifications"


class Database:
    def __init__(self, config: Configuration, is_local: bool = False):
        URI = config.LOCAL_URI if is_local else config.REMOTE_URI
        self.client = AsyncMongoClient(
            URI,
            server_api=ServerApi("1"),
            maxPoolSize=20,  # decrease max pool size
            minPoolSize=5,  # Set min pool size
            maxIdleTimeMS=30000,  # 30 seconds idle timeout
            connectTimeoutMS=20000,  # 20 seconds connect timeout
            serverSelectionTimeoutMS=20000,
            socketTimeoutMS=20000,
            retryWrites=True,
            w="majority",
        )

        self.db = self.client.agrismart  # name of the database

    def ping(self):
        return self.client.admin.command("ping")

    def collections(self):
        return self.db.list_collection_names()

    def get_collection(self, name: CollectionName) -> AsyncCollection:
        collection = self.db[name.value]
        return collection

    async def close(self):
        await self.client.close()
