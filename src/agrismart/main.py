import os
from fastapi import FastAPI
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.configuration import Configuration
from core.exceptions import ErrorCodes, ExceptionHandler
from core.secures import Cryptography, KeyBackend
from infrastructure.apis import Cloudinary
from infrastructure.queues import RabbitMQConnection

from agrismart.routers.v1.routes import router as v1
from agrismart.routers.v2.routes import router as v2
from agrismart.middlewares import RateLimitingMiddleware, TracingMiddleware
from agrismart.dependencies import augmenter_monitor


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    config = Configuration()
    await augmenter_monitor(config)

    # Create shared instances
    directory = os.path.join(os.getcwd(), "keys")
    cryptography = Cryptography(
        directory,
        KeyBackend.from_string(config.CRYPTO_BACKEND),
        is_override=False,
        is_caching=True,
    )
    cryptography.generate()

    # Initialize RabbitMQ connection
    queue = RabbitMQConnection(config.RABBITMQ_BROKER_URL)
    await queue.connect()
    await queue.start_all_consumers()

    # Store in app state
    app.state.config = config
    app.state.queue = queue
    app.state.cryptography = cryptography

    # Initialize external services
    Cloudinary.setup(config)

    yield

    # Shutdown
    await queue.stop_all_consumers()
    await app.state.queue.disconnect()


app = FastAPI(lifespan=lifespan)


# Initialize CORS middleware
config = Configuration()
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


# Custom exception handlers when validation fails
@app.exception_handler(RequestValidationError)
async def custom_request_validation_exception_handler(_: Request, exc: RequestValidationError):
    raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exc))


# Custom exception handler for general exceptions
@app.exception_handler(ExceptionHandler)
async def exception_handler(_: Request, exc: ExceptionHandler):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "statusCode": exc.statusCode(),
            "message": exc.msg,
        },
        headers={"X-Error": f"{status.HTTP_200_OK}.{exc.code}"},
        media_type="application/json",
        # write log here
    )
