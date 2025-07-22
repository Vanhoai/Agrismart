from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse

from core.exceptions import ExceptionHandler

from agrismart.routers.v1.routes import router as v1
from agrismart.routers.v2.routes import router as v2

from agrismart.dependencies import build_config

# init application
app = FastAPI()

# middlewares
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in build_config().CORS_ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1, prefix="/api/v1")
app.include_router(v2, prefix="/api/v2")


# exception
@app.exception_handler(ExceptionHandler)
async def exception_handler(_: Request, exc: ExceptionHandler):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "message": exc.msg,
        },
        headers={"X-Error": f"{status.HTTP_200_OK}.{exc.code}"},
        media_type="application/json",
        # write log here
    )
