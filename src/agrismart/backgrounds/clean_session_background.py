import time
from loguru import logger
from pymongo.asynchronous.collection import AsyncCollection

from .background_task import BackgroundTask


class CleanSessionBackground(BackgroundTask):
    def __init__(
        self,
        interval: int,
        collection: AsyncCollection,
    ):
        super().__init__(
            name="Clean Session",
            is_enabled=True,
            interval=interval,
        )
        self.collection = collection

    async def run_task(self):
        sessions = await self.collection.delete_many({"expired_at": {"$lt": time.time()}})
        logger.info(f"Cleaned {sessions.deleted_count} expired sessions from the database")
