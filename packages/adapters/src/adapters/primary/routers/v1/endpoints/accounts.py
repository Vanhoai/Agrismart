from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from domain.usecases import FindAccountsQuery, CreateAccountRequest, FindAccountByEmailQuery, CreateProviderParams
from domain.services import AccountService
from domain.entities import EnumRole, AccountEntity

from adapters.primary import auth_middleware, role_middleware
from adapters.primary import auto_response_decorator, exception_decorator

from adapters.shared.dependencies import build_account_service

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.get("/find-by-email")
@exception_decorator
@auto_response_decorator(
    message="Account retrieved successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def find_account_by_email(
    query: Annotated[FindAccountByEmailQuery, Query()],
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.find_by_email(query)


@router.get("/find-profile")
@exception_decorator
@auto_response_decorator(
    message="Account profile retrieved successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def find_account_profile(
    account: AccountEntity = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.find_by_id(str(account.id))


@router.post("/{account_id}/create-provider")
@exception_decorator
@auto_response_decorator(
    message="Provider created successfully 🐳",
    status_code=status.HTTP_201_CREATED,
)
async def create_provider(
    account_id: str,
    params: CreateProviderParams,
    account: AccountEntity = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.create_provider(account_id, params)


@router.get("/{account_id}")
@exception_decorator
@auto_response_decorator(
    message="Account retrieved successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def find_account_by_id(
    account_id: str,
    account: AccountEntity = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.find_by_id(account_id)


@router.get("/")
@exception_decorator
@auto_response_decorator(
    message="Accounts retrieved successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def find_accounts(
    query: Annotated[FindAccountsQuery, Query()],
    account: AccountEntity = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.find_accounts(query)


@router.post("/")
@exception_decorator
@auto_response_decorator(
    message="Account created successfully 🐳",
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    req: CreateAccountRequest,
    account: AccountEntity = Depends(auth_middleware),
    passed: bool = Depends(role_middleware(required=[EnumRole.SUPER])),
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.create_account(req)
