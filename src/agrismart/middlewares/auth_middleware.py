from fastapi import Depends, Request

from core.secures import Jwt, JwtPayload, KeyType
from core.exceptions import ErrorCodes, ExceptionHandler
from domain.services import AccountService

from agrismart.dependencies import build_account_service, build_jwt


async def required_authentication(req: Request, jwt: Jwt) -> JwtPayload:
    authorization = req.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        raise ExceptionHandler(code=ErrorCodes.UNAUTHORIZED, msg="Invalid or missing Bearer token 👀")

    token = authorization.removeprefix("Bearer ").strip()
    claims = jwt.decode(token, KeyType.ACCESS)
    return claims


async def func(
    req: Request,
    jwt: Jwt = Depends(build_jwt),
    account_service: AccountService = Depends(build_account_service),
) -> JwtPayload:
    try:
        claims = await required_authentication(req, jwt)

        req.state.account = {}
        return claims
    except Exception as exception:
        raise ExceptionHandler(code=ErrorCodes.UNAUTHORIZED, msg=str(exception))
