from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel
from domain.entities import AccountEntity


class OAuthRequest(CamelModel):
    id_token: str
    raw_nonce: str
    device_token: str


class AuthUseCase(ABC):
    @abstractmethod
    async def oauth(self, req: OAuthRequest) -> AccountEntity: ...

    @abstractmethod
    async def face_auth(self): ...
