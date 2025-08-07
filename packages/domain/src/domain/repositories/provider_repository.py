from domain.entities import ProviderEntity
from domain.repositories import IBaseRepository


class IProviderRepository(IBaseRepository[ProviderEntity]):
    pass
