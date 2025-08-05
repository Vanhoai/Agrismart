from .base_entity import BaseEntity
from core.helpers import TimeHelper


class SessionEntity(BaseEntity):
    account_id: str
    access_token_jti: str
    refresh_token: str
    expired_at: int
    device_token: str
    ip_address: str

    @staticmethod
    def create(
        account_id: str,
        access_token_jti: str,
        refresh_token: str,
        expired_at: int,
        device_token: str,
        ip_address: str,
    ) -> "SessionEntity":
        return SessionEntity(
            account_id=account_id,
            access_token_jti=access_token_jti,
            refresh_token=refresh_token,
            expired_at=expired_at,
            device_token=device_token,
            ip_address=ip_address,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
