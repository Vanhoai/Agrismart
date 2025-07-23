from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel

from domain.entities import EnumRole, RoleEntity


class CreateRoleRequest(CamelModel):
    account_id: str
    role: EnumRole


class ManageRoleUseCase(ABC):
    @abstractmethod
    async def create_role(self, request: CreateRoleRequest) -> RoleEntity: ...
