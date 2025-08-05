from pydantic import Field
from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel


# ============================== AUTH USE CASES ==============================
class OAuthRequest(CamelModel):
    id_token: str
    raw_nonce: str


class AuthResponse(CamelModel):
    access_token: str
    refresh_token: str


class AuthWithEmailPasswordRequest(CamelModel):
    email: str
    password: str = Field(min_length=5)


class ManageSignInUseCase(ABC):
    @abstractmethod
    async def oauth(self, req: OAuthRequest) -> AuthResponse: ...

    @abstractmethod
    async def face_auth(self): ...

    @abstractmethod
    async def auth_with_email_password(self, req: AuthWithEmailPasswordRequest) -> AuthResponse: ...


# ============================== MANAGE AUTH SESSION USE CASE ==============================
class RefreshTokenParams(CamelModel):
    refresh_token: str


class ManageAuthSessionUseCase(ABC):
    @abstractmethod
    async def refresh_token(self, params: RefreshTokenParams) -> AuthResponse: ...
