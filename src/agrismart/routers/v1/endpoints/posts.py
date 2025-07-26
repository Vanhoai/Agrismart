from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.base import HttpResponse
from core.secures import JwtPayload

from domain.services.post_service import PostService
from domain.usecases import CreatePostRequest

from agrismart.dependencies import build_post_service
from agrismart.decorators import exception_decorator
from agrismart.middlewares import auth_middleware, role_middleware


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post("/")
@exception_decorator
async def create_post(
    req: CreatePostRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
    post_service: PostService = Depends(build_post_service),
):
    account = await post_service.create_post(claims.id, req)
    http_response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Created post successfully 🐳",
        data=account,
    )

    return JSONResponse(content=jsonable_encoder(http_response))
