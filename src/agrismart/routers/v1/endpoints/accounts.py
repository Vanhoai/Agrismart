from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.secures import JwtPayload
from core.base import HttpPaginationResponse, HttpResponse
from core.exceptions import ErrorCodes, ExceptionHandler

from domain.usecases import FindAccountsQuery, CreateAccountRequest
from domain.services import AccountService
from domain.entities import EnumRole

from agrismart.dependencies import build_account_service
from agrismart.middlewares import auth_middleware, role_middleware
from agrismart.decorators import exception_decorator


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.get("/")
@exception_decorator
async def find_accounts(
    query: Annotated[FindAccountsQuery, Query()],
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    accounts, meta = await account_service.find_accounts(query)
    response = HttpPaginationResponse(
        status_code=status.HTTP_200_OK,
        message="Accounts retrieved successfully 🐳",
        meta=meta,
        data=accounts,
    )

    return JSONResponse(content=jsonable_encoder(response))


@router.get("/{id}")
@exception_decorator
async def find_account_by_id(
    id: str,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    account = await account_service.find_by_id(id)
    response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Account retrieved successfully 🐳",
        data=account,
    )

    return JSONResponse(content=jsonable_encoder(response))


@router.post("/")
@exception_decorator
async def create_account(
    req: CreateAccountRequest,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[EnumRole.SUPER])),
    account_service: AccountService = Depends(build_account_service),
):
    account = await account_service.create_account(req)
    response = HttpResponse(
        status_code=status.HTTP_201_CREATED,
        message="Account created successfully 🐳",
        data=account,
    )

    return JSONResponse(content=jsonable_encoder(response))
