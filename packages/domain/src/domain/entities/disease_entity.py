from core.helpers import TimeHelper
from domain.entities import BaseEntity


class DiseaseEntity(BaseEntity):
    name: str
    description: str

    @staticmethod
    def create(name: str, description: str) -> "DiseaseEntity":
        return DiseaseEntity(
            _id=None,
            name=name,
            description=description,
            created_at=TimeHelper.vn_timezone(),
            updated_at=TimeHelper.vn_timezone(),
            deleted_at=None,
        )
