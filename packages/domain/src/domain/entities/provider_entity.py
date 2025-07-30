from enum import Enum

from core.helpers import TimeHelper
from .base_entity import BaseEntity


class EnumProvider(Enum):
    GOOGLE = "google"
    GITHUB = "github"
    AZURE = "azure"


class ProviderEntity(BaseEntity):
    account_id: str
    provider: str
    provider_id: str

    @staticmethod
    def create(account_id: str, provider: EnumProvider, provider_id: str) -> "ProviderEntity":
        return ProviderEntity(
            _id=None,
            account_id=account_id,
            provider=provider.value,
            provider_id=provider_id,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
