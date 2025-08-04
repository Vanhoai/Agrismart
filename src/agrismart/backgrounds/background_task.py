import asyncio
import time
from typing import Optional
from abc import ABC, abstractmethod
from loguru import logger


class BackgroundTask(ABC):
    def __init__(
        self,
        name: str,
        is_enabled: bool = True,
        interval: int = 30
    ):
        self.name = name
        self.is_enabled = is_enabled
        self.interval = interval

        self.is_running = None
        self.task: Optional[asyncio.Task] = None

    @abstractmethod
    async def run_task(self):
        ...

    async def _create_schedule(self):
        logger.info(f"{self.name} will run every {self.interval} seconds")
        while self.is_running:
            try:
                start_time = time.time()
                start_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
                logger.info(f"Starting task {self.name} at {start_time_formatted}")
                await self.run_task()
                end_time = time.time()
                duration = end_time - start_time

                logger.info(f"Task {self.name} completed in {duration:.2f} seconds")

                next_sync_time = time.time() + self.interval
                next_sync_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_sync_time))
                logger.info(f"Next sync in {next_sync_time_formatted} seconds")

                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                logger.info(f"Task {self.name} was cancelled 👋🏻")
                break
            except Exception as exception:
                logger.error(f"Error in task {self.name}: {exception}")
                await asyncio.sleep(300)

    async def start(self):
        if not self.is_enabled:
            logger.info(f"Background task {self.name} is disabled 🫠, skipping initialization")
            return

        if self.is_running:
            logger.info(f"Background task {self.name} is already running 😵‍💫")
            return

        self.is_running = True
        self.task = asyncio.create_task(self._create_schedule())

    async def stop(self):
        if not self.is_enabled:
            logger.info(f"Background task {self.name} is disabled 🤧, skipping shutdown")
            return

        if not self.is_running:
            return

        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                logger.info(f"Background task {self.name} stopped 👋🏻")
