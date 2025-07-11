from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel

class SignInRequest(CamelModel):
    id_token: str
    device_token: str

class SignInResponse(CamelModel):
    access_token: str
    refresh_token: str

class AuthUseCase(ABC):
    @abstractmethod
    async def sign_in(self, req: SignInRequest) -> SignInResponse: ...
