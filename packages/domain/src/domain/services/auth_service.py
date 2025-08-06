import uuid
import asyncio
from typing import Tuple
from fastapi import Depends
from argon2 import PasswordHasher
from bson import ObjectId

from core.configuration import Configuration
from core.secures import Jwt, JwtPayload, KeyType
from core.helpers import TimeHelper
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.usecases import (
    ManageSignInUseCase,
    OAuthRequest,
    AuthResponse,
    AuthWithEmailPasswordRequest,
    ManageAuthSessionUseCase,
)
from domain.usecases.auth_usecases import RefreshTokenParams
from domain.repositories import AccountRepository, SessionRepository, ProviderRepository
from domain.entities import AccountEntity, SessionEntity, ProviderEntity, EnumProvider

from infrastructure.apis import Supabase
from infrastructure.models import UserSupabaseMetadata


class AuthService(ManageSignInUseCase, ManageAuthSessionUseCase):
    def __init__(
        self,
        account_repository: AccountRepository = Depends(),
        session_repository: SessionRepository = Depends(),
        provider_repository: ProviderRepository = Depends(),
        supabase: Supabase = Depends(),
        jwt: Jwt = Depends(),
        config: Configuration = Depends(),
    ):
        self.account_repository = account_repository
        self.session_repository = session_repository
        self.provider_repository = provider_repository
        self.supabase = supabase
        self.jwt = jwt
        self.config = config

    async def _sign_tokens(self, account: AccountEntity) -> Tuple[str, str, str]:
        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + self.config.ACCESS_TOKEN_EXPIRATION)
        iat = int(timestamp)

        jti = str(uuid.uuid4())
        access_payload: JwtPayload = JwtPayload(
            exp=exp,
            iat=iat,
            jti=jti,
            email=account.email,
            account_id=str(account.id),
        )
        refresh_payload: JwtPayload = access_payload.clone(exp=int(timestamp + self.config.REFRESH_TOKEN_EXPIRATION))

        access_token = self.jwt.encode(access_payload, KeyType.ACCESS)
        refresh_token = self.jwt.encode(refresh_payload, KeyType.REFRESH)

        return jti, access_token, refresh_token

    async def _sign_tokens_and_create_session(
        self,
        account: AccountEntity,
        device_token: str,
        ip_address: str,
    ) -> AuthResponse:
        jti, access_token, refresh_token = await self._sign_tokens(account)

        timestamp = TimeHelper.vn_timezone().timestamp()
        session = SessionEntity.create(
            account_id=str(account.id),
            access_token_jti=jti,
            refresh_token=refresh_token,
            expired_at=int(timestamp + self.config.REFRESH_TOKEN_EXPIRATION),
            device_token=device_token,
            ip_address=ip_address,
        )

        # create session
        await self.session_repository.create(session)
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def oauth(self, req: OAuthRequest) -> AuthResponse:
        user_supabase: UserSupabaseMetadata = self.supabase.sign_in_google(
            req.id_token,
            req.raw_nonce,
        )

        account = await self.account_repository.find_one({"email": user_supabase.email})
        if account:
            google_provider = await self.provider_repository.find_one(
                {
                    "account_id": ObjectId(account.id),
                    "provider": EnumProvider.GOOGLE.value,
                }
            )

            if not google_provider:
                raise ExceptionHandler(
                    ErrorCodes.REQUIRED_AUTHENTICATION,
                    "Please sign in with email and password first, then enable Google OAuth in Settings 🥺",
                )
        else:
            account_entity = AccountEntity.create(
                username=user_supabase.name,
                password=None,
                email=user_supabase.email,
                avatar=user_supabase.avatar_url,
            )

            # create new account
            account = await self.account_repository.create(account_entity)

            # create provider for account
            provider_entity = ProviderEntity.create(
                account_id=str(account.id),
                provider=EnumProvider.GOOGLE,
                uid=user_supabase.uid,
            )

            await self.provider_repository.create(provider_entity)

        return await self._sign_tokens_and_create_session(
            account=account,
            device_token=req.device_token,
            ip_address=req.ip_address,
        )

    async def auth_with_email_password(self, req: AuthWithEmailPasswordRequest) -> AuthResponse:
        account = await self.account_repository.find_one({"email": req.email})
        ph = PasswordHasher()
        if account is None:
            password_hash = ph.hash(req.password)

            account_entity = AccountEntity.create(
                username=req.email.split("@")[0],
                email=req.email,
                password=password_hash,
                avatar="https://i.pinimg.com/736x/ca/77/fa/ca77fadb377a2e583a1cc881d0d9e236.jpg",
            )

            # create new account
            account = await self.account_repository.create(account_entity)
        else:
            if account.password is None:
                # reset password
                raise ExceptionHandler(ErrorCodes.BAD_REQUEST, "Account have social provider, please reset password 🥺")

            # verify password
            if not ph.verify(account.password, req.password):
                raise ExceptionHandler(ErrorCodes.BAD_REQUEST, "Your password is incorrect, please try again 🤧")

        return await self._sign_tokens_and_create_session(
            account=account,
            device_token=req.device_token,
            ip_address=req.ip_address,
        )

    async def refresh_token(self, params: RefreshTokenParams) -> AuthResponse:
        payload = self.jwt.decode(params.refresh_token, KeyType.REFRESH)
        if not payload:
            raise ExceptionHandler(
                code=ErrorCodes.UNAUTHORIZED,
                msg="Your refresh token is invalid, please sign in again 🥺",
            )

        account = await self.account_repository.find_one({"email": payload.email})
        if not account:
            raise ExceptionHandler(
                code=ErrorCodes.UNAUTHORIZED,
                msg="Your account does not exist, please sign up again 🥺",
            )

        jti, access_token, refresh_token = await self._sign_tokens(account)
        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + self.config.REFRESH_TOKEN_EXPIRATION)

        session = SessionEntity.create(
            account_id=str(account.id),
            access_token_jti=jti,
            refresh_token=refresh_token,
            expired_at=exp,
            device_token=params.device_token,
            ip_address=params.ip_address,
        )

        tasks = [
            self.session_repository.create(session),
            self.session_repository.delete_one({"access_token_jti": payload.jti}),
        ]
        await asyncio.gather(*tasks)
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def sign_out(self, account_id: str) -> bool:
        await self.session_repository.delete_many({"account_id": ObjectId(account_id)})
        return True
