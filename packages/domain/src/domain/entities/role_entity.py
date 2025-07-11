from enum import Enum

from domain.entities import BaseEntity

class EnumRole(Enum):
    NORMAL = 1
    ADMIN = 2

class RoleEntity(BaseEntity):
    account_id: str
    role: int

    def __init__(self, account_id: str, role: EnumRole = EnumRole.NORMAL):
        super().__init__()
        self.account_id = account_id
        self.role = role.value

    @staticmethod
    def from_dict(account_id: str, role: EnumRole = EnumRole.NORMAL):
        return RoleEntity(account_id=account_id, role=role)
