from tabulate import tabulate
from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.accounts import router as accounts_router
from .endpoints.roles import router as roles_router
from .endpoints.posts import router as posts_router
from .endpoints.medias import router as medias_router
from .endpoints.diagnostics import router as diagnostics_router

router = APIRouter()
routes = [auth_router, accounts_router, roles_router, posts_router, medias_router, diagnostics_router]


def format_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("_"))


def format_method(methods: set) -> str:
    if not methods:
        return "N/A"

    return ", ".join(method.upper() for method in methods if method != "HEAD")


table = []
for route in routes:
    router.include_router(route)
    for r in route.routes:
        name = format_name(r.name)  # type: ignore
        method = format_method(r.methods)  # type: ignore
        row = ["/api/v1", method, r.path, name]  # type: ignore
        table.append(row)

print(
    tabulate(
        table,
        headers=["Version", "Method", "Path", "Name"],
        tablefmt="pretty",
        colalign=("center", "center", "left", "left"),
    ),
)
