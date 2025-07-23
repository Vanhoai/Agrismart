from fastapi import APIRouter, Depends, Query, status
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from agrismart.dependencies import build_account_service
from agrismart.middlewares import auth_middleware, role_middleware

from domain.usecases import FindAccountsQuery
from domain.services import AccountService

from core.secures import JwtPayload
from core.base import HttpPaginationResponse, HttpResponse
from core.exceptions import ErrorCodes, ExceptionHandler

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.get("/")
async def find_accounts(
    query: Annotated[FindAccountsQuery, Query()],
    claims: JwtPayload = Depends(auth_middleware.func),
    passed=Depends(role_middleware.func(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    try:
        accounts, meta = await account_service.find_accounts(query)
        response = HttpPaginationResponse(
            status_code=status.HTTP_200_OK,
            message="Accounts retrieved successfully 🐳",
            meta=meta,
            data=accounts,
        )

        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))


@router.get("/{id}")
async def get_account(
    id: str,
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
    account_service: AccountService = Depends(build_account_service),
):
    try:
        account = await account_service.find_by_id(id)
        response = HttpResponse(
            status_code=status.HTTP_200_OK,
            message="Account retrieved successfully 🐳",
            data=account,
        )

        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))
