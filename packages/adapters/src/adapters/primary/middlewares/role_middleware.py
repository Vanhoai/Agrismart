from typing import List
from fastapi import Request, Depends

from agrismart.dependencies import build_role_service

from core.exceptions import ExceptionHandler, ErrorCodes
from domain.entities import EnumRole
from domain.services import RoleService


def role_middleware(required: List[EnumRole] = []):
    async def execute(
        req: Request,
        role_service: RoleService = Depends(build_role_service),
    ) -> bool:
        if len(required) == 0:
            return True

        if not req.state.account:
            raise ExceptionHandler(code=ErrorCodes.NOT_FOUND, msg="Account not found in database 🐔")

        entity = await role_service.find_role_by_account_id(req.state.account.id)
        if not entity:
            raise ExceptionHandler(code=ErrorCodes.FORBIDDEN, msg="You don't have any role assigned to your account 🐶")

        if entity.role not in [role.value for role in required]:
            raise ExceptionHandler(code=ErrorCodes.FORBIDDEN, msg="Not enough permissions to access this resource 🐶")

        return True

    return execute
