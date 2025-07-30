import asyncio
import datetime
from tabulate import tabulate
from loguru import logger
from typing import Optional

from core.configuration import Configuration
from infrastructure.schedulers import SyncScheduler


class SyncBackground:
    def __init__(self, config: Configuration):
        self.config = config
        self.sync_scheduler = SyncScheduler(config)
        self.task: Optional[asyncio.Task] = None
        self.is_running = False

    async def start(self):
        if not self.config.IS_SYNC_DATABASE_ENABLED:
            logger.info("Sync database is disabled 🫠, skipping background scheduler initialization")
            return

        if self.is_running:
            logger.info("Background scheduler already running 😵‍💫")
            return

        self.is_running = True
        self.task = asyncio.create_task(self._run_scheduler())

    async def stop(self):
        if not self.config.IS_SYNC_DATABASE_ENABLED:
            logger.info("Sync database is disabled 🤧, skipping background scheduler shutdown")
            return

        if not self.is_running:
            return

        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                logger.info("Background scheduler stopped 👋🏻")

        await self.sync_scheduler.close()

    async def _run_scheduler(self):
        interval = self.config.SYNC_DATABASE_INTERVAL * 60  # Convert minutes to seconds
        logger.info(f"Sync background scheduler will run every {interval // 60} seconds")
        while self.is_running:
            try:
                start_time = datetime.datetime.now()
                logger.info(f"Starting sync at {start_time}")
                results = await self.sync_scheduler.sync_collections()

                end_time = datetime.datetime.now()
                duration = (end_time - start_time).total_seconds()

                table = []
                for collection, stats in results.items():
                    table.append([collection, stats["synced"], stats["skipped"], stats["errors"]])  # type: ignore

                end = datetime.datetime.now()
                logger.info(f"Sync background scheduler finished at {end} - Duration: {duration} seconds")
                logger.info(
                    f"Sync results:\n{tabulate(table, headers=["Collection", "Synced", "Skipped", "Errors"], tablefmt="pretty")}"
                )

                logger.info(f"Next sync in {interval // 60} minutes")
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                logger.info("Sync scheduler cancelled")
                break
            except Exception as e:
                logger.error(f"Error in sync scheduler: {e}")
                await asyncio.sleep(300)

    async def run_once(self):
        try:
            logger.info("Running sync manually...")
            results = await self.sync_scheduler.sync_collections()

            total_synced = sum(r.get("synced", 0) for r in results.values())  # type: ignore
            total_skipped = sum(r.get("skipped", 0) for r in results.values())  # type: ignore

            logger.info(f"Manual sync completed - Synced: {total_synced}, Skipped: {total_skipped}")
            return results
        except Exception as e:
            logger.error(f"Error in manual sync: {e}")
            raise
