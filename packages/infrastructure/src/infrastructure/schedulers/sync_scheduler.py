import asyncio
from typing import Dict
from loguru import logger

from core.configuration import Configuration
from core.database import Database, CollectionName


class SyncScheduler:
    def __init__(self, config: Configuration):
        self.config = config
        self.local_db = Database(config, is_local=True)
        self.remote_db = Database(config, is_local=False)

    async def sync_collection(self, collection_name: CollectionName) -> Dict[str, int]:
        local_collection = self.local_db.get_collection(collection_name)
        remote_collection = self.remote_db.get_collection(collection_name)

        # Get all docs from local
        local_docs = await local_collection.find({}).to_list(None)

        synced = 0
        skipped = 0

        for doc in local_docs:
            try:
                # Check if the document exists in the remote collection
                existing = await remote_collection.find_one({"_id": doc["_id"]})
                if existing:
                    # Check if the document has been updated
                    if existing.get("updated_at") != doc.get("updated_at"):
                        await remote_collection.replace_one({"_id": doc["_id"]}, doc)
                        synced += 1
                    else:
                        skipped += 1
                else:
                    # Insert new document
                    await remote_collection.insert_one(doc)
                    synced += 1
            except Exception as e:
                logger.error(f"Error syncing document {doc['_id']}: {e}")
                continue

        return {"synced": synced, "skipped": skipped}

    async def sync_collections(self) -> Dict[str, int]:
        collections_to_sync = [
            CollectionName.ACCOUNTS,
            CollectionName.POSTS,
            CollectionName.ROLES,
        ]

        tasks = []
        for collection_name in collections_to_sync:
            tasks.append(self.sync_collection(collection_name))

        results = {}
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        # noinspection PyTypeChecker
        for i in range(len(collections_to_sync)):
            collection_name = collections_to_sync[i].value
            if isinstance(responses[i], Exception):
                logger.error(f"Error syncing collection {collection_name}: {responses[i]}")
                results[collection_name] = {"synced": 0, "skipped": 0}
            else:
                results[collection_name] = responses[i]

        for collection_name, stats in results.items():
            logger.info(f"Collection {collection_name} - Synced: {stats['synced']}, Skipped: {stats['skipped']}")

        return results

    async def close(self):
        await self.local_db.close()
        await self.remote_db.close()
        print("Databases closed successfully 👋🏻")
