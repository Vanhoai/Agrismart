from abc import ABC, abstractmethod
from fastapi_camelcase import CamelModel
from typing import Tuple, List

from core.base import BaseQuery, Meta
from domain.entities import EnumRole, RoleEntity


class CreateRoleRequest(CamelModel):
    account_id: str
    role: EnumRole


class FindRolesQuery(BaseQuery):
    pass


class ManageRoleUseCase(ABC):
    @abstractmethod
    async def find_roles(self, query: FindRolesQuery) -> Tuple[List[RoleEntity], Meta]: ...

    @abstractmethod
    async def create_role(self, request: CreateRoleRequest) -> RoleEntity: ...

    @abstractmethod
    async def find_role_by_account_id(self, account_id: str) -> RoleEntity: ...
