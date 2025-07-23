from fastapi import Depends
from bson import ObjectId
from typing import List, Tuple

from core.base import Meta
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.usecases import ManageRoleUseCase, CreateRoleRequest, FindRolesQuery
from domain.repositories import RoleRepository, AccountRepository
from domain.entities import RoleEntity


class RoleService(ManageRoleUseCase):
    def __init__(
        self,
        role_repository: RoleRepository = Depends(),
        account_repository: AccountRepository = Depends(),
    ):
        self.role_repository = role_repository
        self.account_repository = account_repository

    async def create_role(self, request: CreateRoleRequest) -> RoleEntity:
        role = await self.role_repository.find_one({"account_id": ObjectId(request.account_id)})
        if role:
            raise ExceptionHandler(ErrorCodes.ALREADY_EXISTS, f"Role for account {request.account_id} already exists.")

        account = await self.account_repository.find_one({"_id": ObjectId(request.account_id)})

        if not account:
            raise ExceptionHandler(ErrorCodes.NOT_FOUND, f"Account with ID {request.account_id} not found.")

        entity = RoleEntity.create(request.account_id, request.role)
        response = await self.role_repository.create(entity)
        return response

    async def find_role_by_account_id(self, account_id: str) -> RoleEntity:
        role = await self.role_repository.find_one({"account_id": ObjectId(account_id)})
        if not role:
            raise ExceptionHandler(ErrorCodes.NOT_FOUND, f"Role for account {account_id} not found.")

        return role

    async def find_roles(self, query: FindRolesQuery) -> Tuple[List[RoleEntity], Meta]:
        roles, meta = await self.role_repository.paginated(
            {},
            page=query.page,
            page_size=query.page_size,
            order=query.order,
            order_by=query.order_by,
        )

        return roles, meta
