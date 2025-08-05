from abc import ABC, abstractmethod
from core.base import BaseQuery, Meta
from typing import Tuple, List
from fastapi_camelcase import CamelModel
from domain.entities import AccountEntity


class FindAccountsQuery(BaseQuery):
    pass


class CreateAccountRequest(BaseQuery):
    username: str
    email: str
    avatar: str
    device_token: str


class FindAccountByEmailQuery(CamelModel):
    email: str


class ManageAccountUseCase(ABC):
    @abstractmethod
    async def find_accounts(
        self,
        query: FindAccountsQuery,
    ) -> Tuple[List[AccountEntity], Meta]: ...

    @abstractmethod
    async def find_by_id(self, account_id: str) -> AccountEntity: ...

    @abstractmethod
    async def create_account(self, req: CreateAccountRequest) -> AccountEntity: ...

    @abstractmethod
    async def find_by_email(self, req: FindAccountByEmailQuery) -> AccountEntity: ...
