from fastapi import APIRouter, Depends, Query, status
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from agrismart import dependencies

from domain.usecases import FindAccountsQuery
from domain.services import AccountService

from core.base import HttpPaginationResponse
from core.exceptions import ErrorCodes, ExceptionHandler

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.get("/")
async def find_accounts(
    query: Annotated[FindAccountsQuery, Query()],
    account_service: AccountService = Depends(dependencies.build_account_service),
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
