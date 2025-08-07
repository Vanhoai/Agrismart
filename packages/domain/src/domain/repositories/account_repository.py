from domain.entities import AccountEntity
from domain.repositories import IBaseRepository


class IAccountRepository(IBaseRepository[AccountEntity]):
    pass
