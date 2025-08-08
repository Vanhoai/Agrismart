from fastapi import APIRouter

router = APIRouter()
routes = []

for route in routes:
    router.include_router(route)
