from fastapi import Depends

from domain.repositories import AccountRepository, RoleRepository
from domain.services import AuthService

async def account_repository() -> AccountRepository:
    return AccountRepository()

async def role_repository() -> RoleRepository:
    return RoleRepository()

async def auth_service(
    account_repository: AccountRepository = Depends(account_repository)
) -> AuthService:
    return AuthService(account_repository=account_repository)
