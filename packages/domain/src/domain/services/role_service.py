from fastapi import Depends
from bson import ObjectId

from core.exceptions import ExceptionHandler, ErrorCodes

from domain.usecases import ManageRoleUseCase, CreateRoleRequest
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

        account = await self.account_repository.find_one({
            "_id": ObjectId(request.account_id)
        })

        if not account:
            raise ExceptionHandler(ErrorCodes.NOT_FOUND, f"Account with ID {request.account_id} not found.")

        entity = RoleEntity.create(request.account_id, request.role)
        response = await self.role_repository.create(entity)
        return response
