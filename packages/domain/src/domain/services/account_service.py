from typing import List, Tuple
from core.base import Meta
from domain.entities import AccountEntity
from fastapi import Depends

from domain.usecases import ManageAccountUseCase, FindAccountsQuery
from domain.repositories import AccountRepository


class AccountService(ManageAccountUseCase):
    def __init__(
        self,
        account_repository: AccountRepository = Depends(),
    ):
        self.account_repository = account_repository

    async def find_accounts(
        self,
        query: FindAccountsQuery,
    ) -> Tuple[List[AccountEntity], Meta]:
        accounts, meta = await self.account_repository.find_accounts()
        print(f"Accounts: {accounts}, Meta: {meta}")

        return [], Meta.empty()
