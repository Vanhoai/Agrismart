from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.secures.jwt import JwtPayload
from core.base import HttpResponse, HttpPaginationResponse
from core.exceptions import ExceptionHandler, ErrorCodes
from domain.entities import EnumRole
from domain.usecases import CreateRoleRequest, FindRolesQuery
from domain.services import RoleService

from agrismart.middlewares import auth_middleware, role_middleware
from agrismart.dependencies import build_role_service

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


@router.post("/")
async def create_role(
    body: CreateRoleRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed=Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    try:
        entity = await role_service.create_role(body)
        response = HttpResponse(
            status_code=status.HTTP_201_CREATED,
            message="Role created successfully 🐳",
            data=entity,
        )

        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))


@router.get("/")
async def find_roles(
    query: Annotated[FindRolesQuery, Query()],
    claims: JwtPayload = Depends(auth_middleware.func),
    passed=Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    try:
        roles, meta = await role_service.find_roles(query)
        response = HttpPaginationResponse(
            status_code=status.HTTP_200_OK,
            message="Roles retrieved successfully 🐳",
            meta=meta,
            data=roles,
        )

        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))
