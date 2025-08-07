from fastapi import APIRouter, Depends, status, File, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Literal

from core.secures import JwtPayload
from core.base import HttpResponse
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.services import MediaService
from domain.usecases import UploadMediaRequest

from adapters.shared.dependencies import build_media_service
from adapters.primary import auth_middleware, role_middleware
from adapters.primary import exception_decorator


router = APIRouter(
    prefix="/medias",
    tags=["Medias"],
)


@router.post("/upload")
@exception_decorator
async def upload_media(
    file: Annotated[bytes, File()],
    folder: Annotated[str, Form()],
    media_type: Annotated[str, Form()],
    claims: JwtPayload = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    media_service: MediaService = Depends(build_media_service),
):
    req = UploadMediaRequest.model_validate({"folder": folder, "media_type": media_type})
    response = await media_service.upload_media(file, req)
    response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Accounts retrieved successfully 🐳",
        data=response,
    )

    return JSONResponse(content=jsonable_encoder(response))
