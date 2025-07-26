from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel
from domain.entities import AccountEntity


class OAuthRequest(CamelModel):
    id_token: str
    raw_nonce: str
    device_token: str


class AuthResponse(CamelModel):
    access_token: str
    refresh_token: str


class SignInWithEmailRequest(CamelModel):
    email: str


class AuthUseCase(ABC):
    @abstractmethod
    async def oauth(self, req: OAuthRequest) -> AuthResponse: ...

    @abstractmethod
    async def face_auth(self): ...

    @abstractmethod
    async def sign_in_with_email(self, req: SignInWithEmailRequest) -> AuthResponse: ...
