from fastapi import Depends

from domain.usecases import AuthUseCase, OAuthRequest, OAuthResponse
from domain.repositories import AccountRepository
from domain.entities import AccountEntity

from infrastructure.apis import Supabase
from infrastructure.models import UserSupabaseMetadata


class AuthService(AuthUseCase):
    def __init__(
        self,
        account_repository: AccountRepository = Depends(),
        supabase: Supabase = Depends(),
    ):
        self.account_repository = account_repository
        self.supabase = supabase

    async def oauth(self, req: OAuthRequest) -> OAuthResponse:
        user_supabase: UserSupabaseMetadata = self.supabase.sign_in_google(
            req.id_token,
            req.raw_nonce,
        )

        print(f"User Supabase Metadata: {user_supabase}")

        account = await self.account_repository.find_by_email(user_supabase.email)
        # if account not found -> create new account
        if not account:
            account_entity = AccountEntity.create(
                username=user_supabase.name,
                email=user_supabase.email,
                avatar=user_supabase.avatar_url,
                device_token=req.device_token,
            )

            # account = await self.account_repository.create(account_entity)
            print(f"Account created: {account_entity}")

        return OAuthResponse(
            access_token="dummy_access",
            refresh_token="dummy_refresh",
        )

    async def face_auth(self):
        pass
