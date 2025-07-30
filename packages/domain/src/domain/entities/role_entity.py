from enum import Enum

from core.helpers import TimeHelper
from domain.entities import BaseEntity


class EnumRole(Enum):
    FARMER = 0
    PROFESSOR = 1
    ADMIN = 2
    SUPER = 100


class RoleEntity(BaseEntity):
    account_id: str
    role: int

    @staticmethod
    def create(account_id: str, role: EnumRole) -> "RoleEntity":
        return RoleEntity(
            _id=None,
            account_id=account_id,
            role=role.value,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
