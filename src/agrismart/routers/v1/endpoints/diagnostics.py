from core.secures.jwt import JwtPayload
from fastapi import APIRouter, File, Depends, status
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.base import HttpResponse
from domain.services import DiagnosticService

from agrismart.decorators import exception_decorator
from agrismart.dependencies import build_diagnostic_service
from agrismart.middlewares import auth_middleware, role_middleware

router = APIRouter(
    prefix="/diagnostics",
    tags=["Diagnostics"],
)


@router.post("/")
@exception_decorator
async def diagnostic(
    file: Annotated[bytes, File()],
    claims: JwtPayload = Depends(auth_middleware.func),
    passed: bool = Depends(role_middleware.func(required=[])),
    diagnostic_service: DiagnosticService = Depends(build_diagnostic_service),
):
    diagnostic = await diagnostic_service.diagnose(file)
    response = HttpResponse(
        status_code=status.HTTP_200_OK,
        message="Diagnostic completed successfully ✅",
        data=diagnostic,
    )

    return JSONResponse(content=jsonable_encoder(response))
