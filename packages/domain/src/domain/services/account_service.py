from bson import ObjectId
from typing import List, Tuple
from fastapi import Depends

from core.base import Meta
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.entities import AccountEntity
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
        skip = (query.page - 1) * query.page_size
        limit = query.page_size

        query_dict = {
            "email": {
                "$regex": query.search,
                "$options": "i",
            },
        }

        accounts, records = await self.account_repository.paginated(
            query_dict,
            skip=skip,
            limit=limit,
            order=query.order,
            order_by=query.order_by,
        )

        total_page = (records // query.page_size) + (1 if records % query.page_size > 0 else 0)

        meta = Meta(
            page=query.page,
            page_size=query.page_size,
            total_record=records,
            total_page=total_page,
        )

        return accounts, meta

    async def find_by_id(self, id: str) -> AccountEntity:
        account = await self.account_repository.find_one({"_id": ObjectId(id)})
        if not account:
            raise ExceptionHandler(code=ErrorCodes.NOT_FOUND, msg=f"Account with ID {id} not found.")

        return account
