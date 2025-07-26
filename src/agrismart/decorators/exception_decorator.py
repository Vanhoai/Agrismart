from functools import wraps
from core.exceptions import ExceptionHandler, ErrorCodes


def exception_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ExceptionHandler:
            # Re-raise ExceptionHandler
            raise
        except Exception as exception:
            raise ExceptionHandler(code=ErrorCodes.BAD_REQUEST, msg=str(exception))

    return wrapper
