from core.helpers import TimeHelper
from .base_entity import BaseEntity


class AccountEntity(BaseEntity):
    username: str
    email: str
    avatar: str
    device_token: str

    @staticmethod
    def create(username: str, email: str, avatar: str, device_token: str):
        return AccountEntity(
            _id=None,
            username=username,
            email=email,
            avatar=avatar,
            device_token=device_token,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
