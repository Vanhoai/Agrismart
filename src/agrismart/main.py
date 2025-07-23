import os
import cloudinary
from fastapi import FastAPI
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.exceptions import ExceptionHandler
from core.secures import Cryptography, KeyBackend

from agrismart.routers.v1.routes import router as v1
from agrismart.routers.v2.routes import router as v2
from agrismart.middlewares import RateLimitingMiddleware, TracingMiddleware
from agrismart.dependencies import build_config, augmenter_monitor
from infrastructure.apis import Cloudinary

config = build_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    await augmenter_monitor()

    # Initialize cryptography
    directory = os.path.join(os.getcwd(), "keys")

    # don't override existing keys
    # don't caching keys because it is not needed in this context
    cryptography = Cryptography(directory, KeyBackend.EC, is_override=False, is_caching=False)
    cryptography.generate()

    Cloudinary.setup(config)
    yield
    # Clean up


app = FastAPI(lifespan=lifespan)

# Initialize CORS middleware
origins = [str(origin) for origin in config.CORS_ALLOWED_ORIGINS.split(",")]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TracingMiddleware)
app.add_middleware(RateLimitingMiddleware)

app.include_router(v1, prefix="/api/v1")
app.include_router(v2, prefix="/api/v2")


# exception
@app.exception_handler(ExceptionHandler)
async def exception_handler(_: Request, exc: ExceptionHandler):
    print(f"Exception: {exc}")

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
