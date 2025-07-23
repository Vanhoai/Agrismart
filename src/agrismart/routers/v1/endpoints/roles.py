from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.base import HttpResponse
from core.exceptions import ExceptionHandler, ErrorCodes
from domain.usecases import CreateRoleRequest
from domain.services import RoleService

from agrismart import dependencies

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


@router.post("/")
async def create_role(
    body: CreateRoleRequest,
    role_service: RoleService = Depends(dependencies.build_role_service),
):
    try:
        entity = await role_service.create_role(body)
        response = HttpResponse(
            status_code=status.HTTP_201_CREATED,
            message="Role created successfully 🐳",
            data=entity,
        )

        return JSONResponse(content=jsonable_encoder(response))
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))
