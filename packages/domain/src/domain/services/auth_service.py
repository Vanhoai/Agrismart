from fastapi import Depends

from core.secures import Jwt, JwtPayload, KeyType
from core.helpers import TimeHelper
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.usecases import AuthUseCase, OAuthRequest, AuthResponse, SignInWithEmailRequest
from domain.repositories import AccountRepository
from domain.entities import AccountEntity

from infrastructure.apis import Supabase
from infrastructure.models import UserSupabaseMetadata


class AuthService(AuthUseCase):
    def __init__(
        self,
        account_repository: AccountRepository = Depends(),
        supabase: Supabase = Depends(),
        jwt: Jwt = Depends(),
    ):
        self.account_repository = account_repository
        self.supabase = supabase
        self.jwt = jwt

    # FIXME: update device token and rehandle logic this function
    async def oauth(self, req: OAuthRequest) -> AuthResponse:
        user_supabase: UserSupabaseMetadata = self.supabase.sign_in_google(
            req.id_token,
            req.raw_nonce,
        )

        account = await self.account_repository.find_one({"email": user_supabase.email})
        if not account:
            account_entity = AccountEntity.create(
                username=user_supabase.name,
                email=user_supabase.email,
                avatar=user_supabase.avatar_url,
                device_token=req.device_token,
            )

            account = await self.account_repository.create(account_entity)

        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + 2 * 60 * 60)  # Example expiration time of 1 hour
        iat = int(timestamp)

        payload: JwtPayload = JwtPayload(
            iss="agrismart",
            exp=exp,
            iat=iat,
            id=str(account.id),
            email=account.email,
            device_token=req.device_token,
        )

        access_token = self.jwt.encode(payload, KeyType.ACCESS)
        refresh_token = self.jwt.encode(payload, KeyType.REFRESH)
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def face_auth(self):
        pass

    async def sign_in_with_email(self, req: SignInWithEmailRequest) -> AuthResponse:
        account = await self.account_repository.find_one({"email": req.email})
        if account is None:
            raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg="Account not found")

        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + 2 * 60 * 60)  # Example expiration time of 1 hour
        iat = int(timestamp)

        payload: JwtPayload = JwtPayload(
            iss="agrismart",
            exp=exp,
            iat=iat,
            id=str(account.id),
            email=account.email,
            device_token="",
        )

        access_token = self.jwt.encode(payload, KeyType.ACCESS)
        refresh_token = self.jwt.encode(payload, KeyType.REFRESH)

        return AuthResponse(access_token=access_token, refresh_token=refresh_token)
