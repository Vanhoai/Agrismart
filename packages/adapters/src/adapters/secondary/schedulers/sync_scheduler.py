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
        self.semaphore = asyncio.Semaphore(50)

    async def sync_collection(self, collection_name: CollectionName) -> Dict[str, int]:
        logger.info(f"Starting sync for collection: {collection_name.value}")
        local_collection = self.local_db.get_collection(collection_name)
        remote_collection = self.remote_db.get_collection(collection_name)

        # Get all docs from local
        local_docs = await local_collection.find({}).to_list(None)
        total_docs = len(local_docs)
        logger.info(f"Found {total_docs} documents in {collection_name.value}")

        synced = 0
        skipped = 0
        errors = 0

        # Process documents in batches to avoid too many open connections
        batch_size = 100  # Process 100 documents at a time

        for i in range(0, len(local_docs), batch_size):
            batch = local_docs[i : i + batch_size]
            logger.info(
                f"Processing batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size} "
                f"({len(batch)} documents)"
            )

            tasks = []
            for doc in batch:
                tasks.append(self.sync_document_with_semaphore(remote_collection, doc))

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Error syncing document: {result}")
                    errors += 1
                    continue

                synced += result.get("synced", 0)  # type: ignore
                skipped += result.get("skipped", 0)  # type: ignore

            logger.info(f"Batch completed - Progress: {min(i + batch_size, total_docs)}/{total_docs}")

        logger.info(
            f"Collection {collection_name.value} sync completed - "
            f"Synced: {synced}, Skipped: {skipped}, Errors: {errors}"
        )

        return {"synced": synced, "skipped": skipped, "errors": errors}

    async def sync_document_with_semaphore(self, remote_collection, doc: Dict) -> Dict[str, int]:
        async with self.semaphore:
            return await self.sync_document(remote_collection, doc)

    async def sync_document(self, remote_collection, doc: Dict) -> Dict[str, int]:
        try:
            existing = await remote_collection.find_one({"_id": doc["_id"]})
            if existing:
                if existing.get("updated_at") != doc.get("updated_at"):
                    await remote_collection.replace_one({"_id": doc["_id"]}, doc)
                    return {"synced": 1, "skipped": 0}
                else:
                    return {"synced": 0, "skipped": 1}
            else:
                await remote_collection.insert_one(doc)
                return {"synced": 1, "skipped": 0}
        except Exception as e:
            logger.error(f"Error syncing document {doc['_id']}: {e}")
            return {"synced": 0, "skipped": 0}

    async def sync_collections(self) -> Dict[str, int]:
        collections_to_sync = [
            CollectionName.ACCOUNTS,
            CollectionName.POSTS,
            CollectionName.ROLES,
        ]

        results = {}

        for collection_name in collections_to_sync:
            try:
                logger.info(f"Starting sync for collection: {collection_name.value}")
                collection_result = await self.sync_collection(collection_name)
                results[collection_name.value] = collection_result
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Error syncing collection {collection_name.value}: {e}")
                results[collection_name.value] = {"synced": 0, "skipped": 0, "errors": 1}

        total_synced = sum(r.get("synced", 0) for r in results.values())
        total_skipped = sum(r.get("skipped", 0) for r in results.values())
        total_errors = sum(r.get("errors", 0) for r in results.values())

        logger.info(
            f"Sync completed - Total synced: {total_synced}, " f"skipped: {total_skipped}, errors: {total_errors}"
        )

        return results

    async def close(self):
        await self.local_db.close()
        await self.remote_db.close()
        print("Databases closed successfully 👋🏻")
