from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.accounts import router as accounts_router
from .endpoints.roles import router as roles_router
from .endpoints.posts import router as posts_router
from .endpoints.medias import router as medias_router

router = APIRouter()
routes = [auth_router, accounts_router, roles_router, posts_router, medias_router]

for route in routes:
    router.include_router(route)
