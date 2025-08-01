import uuid
import asyncio
from domain.usecases.auth_usecases import RefreshTokenParams
from fastapi import Depends
from argon2 import PasswordHasher
from bson import ObjectId

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
from domain.repositories import AccountRepository, SessionRepository
from domain.entities import AccountEntity, SessionEntity

from infrastructure.apis import Supabase
from infrastructure.models import UserSupabaseMetadata


class AuthService(ManageSignInUseCase, ManageAuthSessionUseCase):
    def __init__(
        self,
        account_repository: AccountRepository = Depends(),
        session_repository: SessionRepository = Depends(),
        supabase: Supabase = Depends(),
        jwt: Jwt = Depends(),
    ):
        self.account_repository = account_repository
        self.session_repository = session_repository
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
                password=None,
                email=user_supabase.email,
                avatar=user_supabase.avatar_url,
            )

            account = await self.account_repository.create(account_entity)

        jti = str(uuid.uuid4())
        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + 2 * 60 * 60)
        iat = int(timestamp)

        payload: JwtPayload = JwtPayload(
            exp=exp,
            iat=iat,
            jti=jti,
            email=account.email,
            account_id=str(account.id),
        )

        access_token = self.jwt.encode(payload, KeyType.ACCESS)
        refresh_token = self.jwt.encode(payload, KeyType.REFRESH)

        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def face_auth(self):
        pass

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

            account = await self.account_repository.create(account_entity)
        else:
            # if account exists -> check password
            # if password None in database -> account have social provider -> reset password
            # else check password
            if account.password is None:
                raise ExceptionHandler(
                    code=ErrorCodes.BAD_REQUEST,
                    msg="Account have social provider, please reset password 🥺",
                )

            if not ph.verify(account.password, req.password):
                raise ExceptionHandler(
                    code=ErrorCodes.BAD_REQUEST,
                    msg="Your password is incorrect, please try again 🤧",
                )

            # update device token
            account.updated_at = TimeHelper.vn_timezone()
            account = await self.account_repository.update_one(account)

        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + 2 * 60 * 60)
        iat = int(timestamp)

        jti = str(uuid.uuid4())
        payload: JwtPayload = JwtPayload(
            exp=exp,
            iat=iat,
            jti=jti,
            email=account.email,
            account_id=str(account.id),
        )

        access_token = self.jwt.encode(payload, KeyType.ACCESS)
        refresh_token = self.jwt.encode(payload, KeyType.REFRESH)

        session = SessionEntity.create(
            account_id=str(account.id),
            access_token_jti=jti,
            refresh_token=refresh_token,
            expired_at=exp,
            # device_information=req.device_information,
            # ip_address=req.ip_address,
        )

        # delete all sessions of account
        # FIXME: This logic only apply in case allow one session per account
        # if you want to allow multiple sessions, you should remove this logic
        await self.session_repository.delete_many({"account_id": ObjectId(account.id)})
        await self.session_repository.create(session)

        return AuthResponse(access_token=access_token, refresh_token=refresh_token)

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

        jti = str(uuid.uuid4())
        timestamp = TimeHelper.vn_timezone().timestamp()
        exp = int(timestamp + 2 * 60 * 60)
        iat = int(timestamp)

        new_payload: JwtPayload = JwtPayload(
            exp=exp,
            iat=iat,
            jti=jti,
            email=account.email,
            account_id=str(account.id),
        )

        access_token = self.jwt.encode(new_payload, KeyType.ACCESS)
        refresh_token = self.jwt.encode(new_payload, KeyType.REFRESH)

        session = SessionEntity.create(
            account_id=str(account.id),
            access_token_jti=jti,
            refresh_token=refresh_token,
            expired_at=exp,
        )

        print(f"jti: {payload.jti}")
        print(f"new jti: {jti}")

        tasks = [
            self.session_repository.create(session),
            self.session_repository.delete_one({"access_token_jti": payload.jti}),
        ]
        await asyncio.gather(*tasks)

        return AuthResponse(access_token=access_token, refresh_token=refresh_token)
