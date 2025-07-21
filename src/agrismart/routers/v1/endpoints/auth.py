from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.base import HttpResponse
from core.exceptions import ExceptionHandler, ErrorCodes
from domain.usecases import SignInRequest
from domain.services import AuthService

from agrismart import dependencies

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/oauth")
async def oauth(
        body: SignInRequest,
        auth_service: AuthService = Depends(dependencies.auth_service),
):
    try:
        sign_in_response = await auth_service.sign_in(body)
        http_response = HttpResponse(
            status_code=status.HTTP_201_CREATED,
            message="success",
            data=sign_in_response,
        )

        return JSONResponse(content=jsonable_encoder(http_response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))
