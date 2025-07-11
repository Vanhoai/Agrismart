from pymongo import AsyncMongoClient
from enum import Enum
from supabase import create_client, Client

from .configuration import config

class CollectionName(str, Enum):
    ACCOUNTS = "accounts"
    ROLES = "roles"
    SUBMISSIONS = "submissions"
    POSTS = "posts"
    # add other collection names as needed

class Database:
    def __init__(self):
        self.client = AsyncMongoClient(config.URI)
        self.db = self.client.agrismart # name of the database

    def ping(self):
        return self.client.admin.command("ping")

    def collections(self):
        return self.db.list_collection_names()

    def get_collection(self, name: CollectionName):
        collection = self.db[name.value]
        return collection

class Supabase:
    def __init__(self):
        url: str = config.SUPABASE_URL
        key: str = config.SUPABASE_KEY
        self.client: Client = create_client(url, key)

database = Database()
supabase = Supabase()
