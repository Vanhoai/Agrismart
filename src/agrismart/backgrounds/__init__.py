from core.configuration import Configuration
from core.database import Database, CollectionName

from .sync_background import SyncBackground
from .background_task import BackgroundTask
from .clean_session_background import CleanSessionBackground


class ManageBackgroundTasks:
    def __init__(
        self,
        configuration: Configuration,
        database: Database
    ):
        self.configuration = configuration
        self.sync_background = SyncBackground(configuration)
        self.clean_session_background = CleanSessionBackground(
            configuration.CLEAN_SESSION_INTERVAL,
            database.get_collection(CollectionName.SESSIONS)
        )

    async def start(self):
        await self.sync_background.start()
        await self.clean_session_background.start()

    async def stop(self):
        await self.sync_background.stop()
        await self.clean_session_background.stop()


__all__ = ["SyncBackground", "ManageBackgroundTasks", "BackgroundTask", "CleanSessionBackground"]
