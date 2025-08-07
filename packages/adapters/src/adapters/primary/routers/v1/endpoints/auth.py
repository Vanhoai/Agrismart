from domain.entities.account_entity import AccountEntity
from domain.usecases.auth_usecases import RefreshTokenParams
from fastapi import APIRouter, Depends, Request, status

from domain.usecases import OAuthRequest, AuthWithEmailPasswordRequest
from domain.services import AuthService

from adapters.shared.dependencies import build_auth_service
from adapters.primary import exception_decorator, auto_response_decorator
from adapters.primary import auth_middleware, role_middleware

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/auth-with-email")
@exception_decorator
@auto_response_decorator(
    message="Authenticated successfully with email and password ✅",
    status_code=status.HTTP_200_OK,
)
async def auth_with_email(
    req: Request,
    body: AuthWithEmailPasswordRequest,
    auth_service: AuthService = Depends(build_auth_service),
):
    ip_address = req.client.host if req.client else "Unknown"
    body.ip_address = ip_address
    return await auth_service.auth_with_email_password(body)


@router.post("/oauth")
@exception_decorator
@auto_response_decorator(
    message="OAuth authentication successful ✅",
    status_code=status.HTTP_200_OK,
)
async def oauth(
    body: OAuthRequest,
    auth_service: AuthService = Depends(build_auth_service),
):
    return await auth_service.oauth(body)


@router.post("/refresh-token")
@exception_decorator
@auto_response_decorator(
    message="Token refreshed successfully ✅",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    body: RefreshTokenParams,
    auth_service: AuthService = Depends(build_auth_service),
):
    return await auth_service.refresh_token(body)


@router.post("/sign-out")
@exception_decorator
@auto_response_decorator(
    message="Signed out successfully ✅",
    status_code=status.HTTP_200_OK,
)
async def sign_out(
    account: AccountEntity = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    auth_service: AuthService = Depends(build_auth_service),
):
    return await auth_service.sign_out(str(account.id))
