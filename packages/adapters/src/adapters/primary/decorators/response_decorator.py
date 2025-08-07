from functools import wraps
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from core.exceptions import ExceptionHandler, ErrorCodes
from core.base import HttpResponse, HttpPaginationResponse, Meta


def http_response(
    message: str = "Request processed successfully 🐳",
    status_code: int = status.HTTP_200_OK,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)

                response = HttpResponse(
                    status_code=status_code,
                    message=message,
                    data=result,
                )

                return JSONResponse(content=jsonable_encoder(response))

            except ExceptionHandler:
                # Re-raise ExceptionHandler
                raise
            except Exception as exception:
                raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))

        return wrapper

    return decorator


def http_pagination_response(message: str = "Request processed successfully 🐳", status_code: int = status.HTTP_200_OK):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)

                if isinstance(result, tuple) and len(result) == 2:
                    data, meta = result
                    response = HttpPaginationResponse(
                        status_code=status_code,
                        message=message,
                        meta=meta,
                        data=data,
                    )
                else:
                    response = HttpResponse(
                        status_code=status_code,
                        message=message,
                        data=result,
                    )

                return JSONResponse(content=jsonable_encoder(response))

            except ExceptionHandler:
                # Re-raise ExceptionHandler
                raise
            except Exception as exception:
                raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))

        return wrapper

    return decorator


def auto_response_decorator(message: str = "Request processed successfully 🐳", status_code: int = status.HTTP_200_OK):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if isinstance(result, tuple) and len(result) == 2:
                    data, meta = result
                    if isinstance(meta, Meta):
                        response = HttpPaginationResponse(
                            status_code=status_code,
                            message=message,
                            meta=meta,
                            data=data,
                        )
                    else:
                        response = HttpResponse(
                            status_code=status_code,
                            message=message,
                            data=result,
                        )
                else:
                    response = HttpResponse(
                        status_code=status_code,
                        message=message,
                        data=result,
                    )

                return JSONResponse(content=jsonable_encoder(response))

            except ExceptionHandler:
                # Re-raise ExceptionHandler
                raise
            except Exception as exception:
                raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))

        return wrapper

    return decorator
