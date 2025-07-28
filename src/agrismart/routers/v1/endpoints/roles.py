from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.secures.jwt import JwtPayload
from core.base import HttpResponse, HttpPaginationResponse

from domain.entities import EnumRole
from domain.usecases import CreateRoleRequest, FindRolesQuery, UpdateRoleRequest
from domain.services import RoleService

from agrismart.middlewares import auth_middleware, role_middleware
from agrismart.dependencies import build_role_service
from agrismart.decorators import exception_decorator

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.post("/")
@exception_decorator
async def create_role(
    body: CreateRoleRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    entity = await role_service.create_role(body)
    response = HttpResponse(
        status_code=status.HTTP_201_CREATED,
        message="Role created successfully 🐳",
        data=entity,
    )

    return JSONResponse(content=jsonable_encoder(response))


@router.get("/")
@exception_decorator
async def find_roles(
    query: Annotated[FindRolesQuery, Query()],
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.ADMIN, EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    roles, meta = await role_service.find_roles(query)
    response = HttpPaginationResponse(
        status_code=status.HTTP_200_OK,
        message="Roles retrieved successfully 🐳",
        meta=meta,
        data=roles,
    )

    return JSONResponse(content=jsonable_encoder(response))


@router.put("/")
@exception_decorator
async def update_role(
    body: UpdateRoleRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    entity = await role_service.update_role(body)
    response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Role updated successfully 🐳",
        data=entity,
    )

    return JSONResponse(content=jsonable_encoder(response))


@router.delete("/{id}")
@exception_decorator
async def delete_role(
    id: str,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    entity = await role_service.delete_role(id)
    response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Role deleted successfully 🐳",
        data=entity,
    )

    return JSONResponse(content=jsonable_encoder(response))
