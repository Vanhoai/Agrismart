from .base_repository import BaseRepository
from domain.entities import SessionEntity


class SessionRepository(BaseRepository[SessionEntity]):
    def __init__(self, collection):
        super().__init__(collection, SessionEntity)
