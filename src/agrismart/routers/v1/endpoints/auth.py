from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.base import HttpResponse
from core.exceptions import ExceptionHandler, ErrorCodes
from domain.usecases import OAuthRequest
from domain.services import AuthService

from agrismart import dependencies

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/oauth")
async def oauth(
        body: OAuthRequest,
        auth_service: AuthService = Depends(dependencies.build_auth_service),
):
    try:
        oauth_response = await auth_service.oauth(body)
        http_response = HttpResponse(
            status_code=status.HTTP_201_CREATED,
            message="success",
            data=oauth_response,
        )

        return JSONResponse(content=jsonable_encoder(http_response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))


@router.post("/face-auth")
async def face_auth():
    """
    Placeholder for face authentication endpoint.
    This function should be implemented to handle face authentication logic.
    """
    raise NotImplementedError("Face authentication is not yet implemented.")
