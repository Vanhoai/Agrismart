from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.base import HttpResponse
from domain.usecases import OAuthRequest, SignInWithEmailRequest
from domain.services import AuthService

from agrismart.dependencies import build_auth_service
from agrismart.decorators import exception_decorator

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/oauth")
@exception_decorator
async def oauth(
    body: OAuthRequest,
    auth_service: AuthService = Depends(build_auth_service),
):
    account = await auth_service.oauth(body)
    http_response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="OAuth successfully ✅",
        data=account,
    )

    return JSONResponse(content=jsonable_encoder(http_response))


@router.post("/face-auth")
@exception_decorator
async def face_auth():
    """
    Placeholder for face authentication endpoint.
    This function should be implemented to handle face authentication logic.
    """
    raise NotImplementedError("Face authentication is not yet implemented.")


@router.post("/sign-in-with-email")
@exception_decorator
async def sign_in_with_email(
    body: SignInWithEmailRequest,
    auth_service: AuthService = Depends(build_auth_service),
):
    account = await auth_service.sign_in_with_email(body)
    http_response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Sign in with email successfully ✅",
        data=account,
    )

    return JSONResponse(content=jsonable_encoder(http_response))
