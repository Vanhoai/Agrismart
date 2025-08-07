from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.base import HttpResponse
from core.secures import JwtPayload

from domain.services.post_service import PostService
from domain.usecases import CreatePostRequest

from adapters.shared.dependencies import build_post_service
from adapters.primary import exception_decorator, auto_response_decorator
from adapters.primary import auth_middleware, role_middleware

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("/")
@exception_decorator
@auto_response_decorator(
    message="Post created successfully 🐳",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    req: CreatePostRequest,
    claims: JwtPayload = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    post_service: PostService = Depends(build_post_service),
):
    return await post_service.create_post(claims.account_id, req)
