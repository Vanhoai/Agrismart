from typing import Annotated
from fastapi import APIRouter, Depends, status, Query

from core.secures.jwt import JwtPayload

from domain.entities import EnumRole
from domain.usecases import CreateRoleRequest, FindRolesQuery, UpdateRoleRequest
from domain.services import RoleService

from agrismart.middlewares import auth_middleware, role_middleware
from agrismart.dependencies import build_role_service
from agrismart.decorators import exception_decorator, auto_response_decorator

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.post("/")
@exception_decorator
@auto_response_decorator(
    message="Role created successfully 🐳",
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    body: CreateRoleRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    return await role_service.create_role(body)


@router.get("/")
@exception_decorator
@auto_response_decorator(
    message="Roles retrieved successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def find_roles(
    query: Annotated[FindRolesQuery, Query()],
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.ADMIN, EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    return await role_service.find_roles(query)


@router.put("/")
@exception_decorator
@auto_response_decorator(
    message="Role updated successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def update_role(
    body: UpdateRoleRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    return await role_service.update_role(body)


@router.delete("/{role_id}")
@exception_decorator
@auto_response_decorator(
    message="Role deleted successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def delete_role(
    role_id: str,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    role_service: RoleService = Depends(build_role_service),
):
    return await role_service.delete_role(role_id)
