from pymongo.asynchronous.collection import AsyncCollection

from domain.entities import SessionEntity
from domain.repositories import ISessionRepository
from .base_repository import BaseRepository


class SessionRepository(BaseRepository[SessionEntity], ISessionRepository):
    def __init__(self, collection: AsyncCollection):
        super().__init__(collection, SessionEntity)
