from bson import ObjectId
from typing import List, Tuple
from fastapi import Depends

from core.base import Meta
from core.exceptions import ExceptionHandler, ErrorCodes

from domain.entities import AccountEntity, ProviderEntity, EnumProvider
from domain.usecases import (
    ManageAccountUseCase,
    FindAccountsQuery,
    CreateAccountRequest,
    FindAccountByEmailQuery,
    ManageAccountProviderUseCase,
    CreateProviderParams,
)
from domain.repositories import IAccountRepository, IProviderRepository

from adapters.secondary import Supabase


class AccountService(ManageAccountUseCase, ManageAccountProviderUseCase):
    def __init__(
        self,
        account_repository: IAccountRepository = Depends(),
        provider_repository: IProviderRepository = Depends(),
        supabase: Supabase = Depends(),
    ):
        self.account_repository = account_repository
        self.provider_repository = provider_repository
        self.supabase = supabase

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

    async def find_by_id(self, account_id: str) -> AccountEntity:
        account = await self.account_repository.find_one({"_id": ObjectId(account_id)})
        if not account:
            raise ExceptionHandler(code=ErrorCodes.NOT_FOUND, msg=f"Account with ID {id} not found 🥹")

        return account

    async def find_by_email(self, req: FindAccountByEmailQuery) -> AccountEntity:
        account = await self.account_repository.find_one({"email": req.email})
        if not account:
            raise ExceptionHandler(code=ErrorCodes.NOT_FOUND, msg=f"Account with email {req.email} not found 😂")

        return account

    async def create_account(self, req: CreateAccountRequest) -> AccountEntity:
        account_entity = AccountEntity.create(
            username=req.username,
            email=req.email,
            password=None,
            avatar=req.avatar,
        )

        existing_account = await self.account_repository.find_one({"email": req.email})
        if existing_account:
            raise ExceptionHandler(
                code=ErrorCodes.BAD_REQUEST, msg="Please use another email, this email already exists 🥺"
            )

        return await self.account_repository.create(account_entity)

    async def create_provider(self, account_id: str, params: CreateProviderParams) -> ProviderEntity:
        match params.provider:
            case EnumProvider.GOOGLE:
                provider = await self.provider_repository.find_one(
                    {
                        "account_id": ObjectId(account_id),
                        "provider": EnumProvider.GOOGLE.value,
                    }
                )

                if provider:
                    raise ExceptionHandler(
                        code=ErrorCodes.BAD_REQUEST,
                        msg="You don't need to create, because it already exists 🥺",
                    )

                id_token = params.payload.get("idToken")
                raw_nonce = params.payload.get("rawNonce")
                if not id_token or not raw_nonce:
                    raise ExceptionHandler(
                        code=ErrorCodes.BAD_REQUEST,
                        msg="Id Token and Raw Nonce are required for Google OAuth 🤧",
                    )

                user_supabase = self.supabase.sign_in_google(
                    id_token=id_token,
                    raw_nonce=raw_nonce,
                )

                provider_entity = ProviderEntity.create(
                    account_id=account_id,
                    provider=params.provider,
                    uid=user_supabase.uid,
                )

            case _:
                raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg="Unsupported provider type")

        return await self.provider_repository.create(provider_entity)
