from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel


class OAuthRequest(CamelModel):
    id_token: str
    raw_nonce: str
    device_token: str


class OAuthResponse(CamelModel):
    access_token: str
    refresh_token: str


class AuthUseCase(ABC):
    @abstractmethod
    async def oauth(self, req: OAuthRequest) -> OAuthResponse: ...

    @abstractmethod
    async def face_auth(self): ...
