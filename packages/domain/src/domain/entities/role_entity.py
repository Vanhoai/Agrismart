from enum import Enum

from domain.entities import BaseEntity


class EnumRole(Enum):
    FARMER = 0
    PROFESSOR = 1
    SUPER = 100


class RoleEntity(BaseEntity):
    account_id: str
    role: int

    def __init__(self, account_id: str, role: EnumRole = EnumRole.FARMER):
        super().__init__()
        self.account_id = account_id
        self.role = role.value
