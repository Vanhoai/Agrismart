from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from agrismart.routers.v1.routes import router as v1
from agrismart.routers.v2.routes import router as v2

from core.configuration import config

# init application
app = FastAPI()

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.CORS_ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1, prefix="/api/v1")
app.include_router(v2, prefix="/api/v2")
