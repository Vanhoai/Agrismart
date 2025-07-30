from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from core.secures import JwtPayload

from domain.usecases import FindAccountsQuery, CreateAccountRequest, FindAccountByEmailQuery
from domain.services import AccountService
from domain.entities import EnumRole

from agrismart.dependencies import build_account_service
from agrismart.middlewares import auth_middleware, role_middleware
from agrismart.decorators import exception_decorator, auto_response_decorator

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


@router.get("/{account_id}")
@exception_decorator
@auto_response_decorator(
    message="Account retrieved successfully 🐳",
    status_code=status.HTTP_200_OK,
)
async def find_account_by_id(
    account_id: str,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
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
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
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
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    account_service: AccountService = Depends(build_account_service),
):
    return await account_service.create_account(req)
