from fastapi import APIRouter, Depends, status, File, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Literal

from core.secures import JwtPayload
from core.base import HttpResponse
from core.exceptions import ExceptionHandler, ErrorCodes

from agrismart.dependencies import build_media_service
from agrismart.middlewares import auth_middleware, role_middleware
from domain.services import MediaService
from domain.usecases import UploadMediaRequest

router = APIRouter(
    prefix="/medias",
    tags=["medias"],
)


@router.post("/upload")
async def upload_media(
        file: Annotated[bytes, File()],
        folder: Annotated[str, Form()],
        media_type: Annotated[str, Form()],
        claims: JwtPayload = Depends(auth_middleware.func),
        passed=Depends(role_middleware.func(required=[])),
        media_service: MediaService = Depends(build_media_service)
):
    try:
        req = UploadMediaRequest.model_validate({
            "folder": folder,
            "media_type": media_type
        })

        response = await media_service.upload_media(file, req)
        response = HttpResponse(
            status_code=status.HTTP_200_OK,
            message="Accounts retrieved successfully 🐳",
            data=response,
        )

        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))
