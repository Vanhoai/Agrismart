from fastapi import Depends

from domain.usecases import AuthUseCase, SignInRequest, SignInResponse
from domain.repositories import AccountRepository

class AuthService(AuthUseCase):
    def __init__(self, account_repository: AccountRepository = Depends()):
        self.account_repository = account_repository

    async def sign_in(self, req: SignInRequest) -> SignInResponse:
        # FIXME: Implement the sign-in logic here
        print(req)
        return SignInResponse(
            access_token="dummy_access",
            refresh_token="dummy_refresh"
        )
