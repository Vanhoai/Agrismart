from fastapi import APIRouter, Depends, status

from domain.usecases import OAuthRequest, SignInWithEmailPasswordRequest
from domain.services import AuthService

from agrismart.dependencies import build_auth_service
from agrismart.decorators import exception_decorator, auto_response_decorator

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


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


@router.post("/face-auth")
@exception_decorator
async def face_auth():
    """
    Placeholder for face authentication endpoint.
    This function should be implemented to handle face authentication logic.
    """
    raise NotImplementedError("Face authentication is not yet implemented.")


@router.post("/auth-with-email")
@exception_decorator
@auto_response_decorator(
    message="Authenticated successfully with email and password ✅",
    status_code=status.HTTP_200_OK,
)
async def auth_with_email(
    body: SignInWithEmailPasswordRequest,
    auth_service: AuthService = Depends(build_auth_service),
):
    return await auth_service.auth_with_email_password(body)
