from fastapi import Depends

from domain.entities import SessionEntity
from domain.usecases import ManageSessionUseCase, CreateSessionParams
from domain.repositories import ISessionRepository


class SessionService(ManageSessionUseCase):
    def __init__(
        self,
        session_repository: ISessionRepository = Depends(),
    ) -> None:
        self.session_repository = session_repository

    async def create_session(self, params: CreateSessionParams) -> SessionEntity:
        session = SessionEntity(**params.dict())
        return await self.session_repository.create(session)
