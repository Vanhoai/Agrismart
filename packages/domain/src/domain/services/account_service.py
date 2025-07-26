from bson import ObjectId
from typing import List, Tuple
from fastapi import Depends

from core.base import Meta
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.entities import AccountEntity
from domain.usecases import ManageAccountUseCase, FindAccountsQuery, CreateAccountRequest
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
        query_dict = {
            "email": {
                "$regex": query.search,
                "$options": "i",
            },
        }

        accounts, meta = await self.account_repository.paginated(
            query_dict,
            page=query.page,
            page_size=query.page_size,
            order=query.order,
            order_by=query.order_by,
        )

        return accounts, meta

    async def find_by_id(self, id: str) -> AccountEntity:
        account = await self.account_repository.find_one({"_id": ObjectId(id)})
        if not account:
            raise ExceptionHandler(code=ErrorCodes.NOT_FOUND, msg=f"Account with ID {id} not found.")

        return account

    async def create_account(self, req: CreateAccountRequest) -> AccountEntity:
        account_entity = AccountEntity.create(
            username=req.username,
            email=req.email,
            avatar=req.avatar,
            device_token=req.device_token,
        )

        existing_account = await self.account_repository.find_one({"email": req.email})
        if existing_account:
            raise ExceptionHandler(
                code=ErrorCodes.BAD_REQUEST, msg="Please use another email, this email already exists 🥺"
            )

        return await self.account_repository.create(account_entity)
