from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel

from domain.entities import SessionEntity


class CreateSessionParams(CamelModel):
    account_id: str
    access_token_jti: str
    refresh_token_hash: str
    device_information: str
    ip_address: str


class ManageSessionUseCase(ABC):
    @abstractmethod
    async def create_session(self, params: CreateSessionParams) -> SessionEntity: ...
