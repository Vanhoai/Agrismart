from abc import ABC, abstractmethod
from core.base import BaseQuery, Meta
from typing import Tuple, List
from domain.entities import AccountEntity


class FindAccountsQuery(BaseQuery):
    pass


class ManageAccountUseCase(ABC):
    @abstractmethod
    async def find_accounts(
        self,
        query: FindAccountsQuery,
    ) -> Tuple[List[AccountEntity], Meta]: ...

    @abstractmethod
    async def find_by_id(self, id: str) -> AccountEntity: ...
