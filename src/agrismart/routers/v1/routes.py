from fastapi import APIRouter

from .endpoints import auth_router, accounts_router

router = APIRouter()
routes = [auth_router, accounts_router]

for route in routes:
    router.include_router(route)
