from typing import Optional

from core.helpers import TimeHelper
from .base_entity import BaseEntity


# FIXME: Create account response for ignore password in response
class AccountEntity(BaseEntity):
    username: str
    email: str
    password: Optional[str]
    avatar: str

    @staticmethod
    def create(username: str, email: str, password: Optional[str], avatar: str) -> "AccountEntity":
        return AccountEntity(
            username=username,
            email=email,
            password=password,
            avatar=avatar,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
