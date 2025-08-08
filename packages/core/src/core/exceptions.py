from enum import Enum


class ErrorCodes(Enum):
    UNAUTHORIZED = "UNAUTHORIZED"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_OPERATION = "INVALID_OPERATION"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    REQUIRED_AUTHENTICATION = "REQUIRED_AUTHENTICATION"
    FILE_SIZE_EXCEEDED = "FILE_SIZE_EXCEEDED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"


class ExceptionHandler(Exception):
    def __init__(self, code: ErrorCodes, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(msg)

    def statusCode(self) -> int:
        status_codes = {
            ErrorCodes.BAD_REQUEST: 400,
            ErrorCodes.UNAUTHORIZED: 401,
            ErrorCodes.FORBIDDEN: 403,
            ErrorCodes.NOT_FOUND: 404,
            ErrorCodes.ALREADY_EXISTS: 409,
            ErrorCodes.CONFLICT: 409,
            ErrorCodes.INVALID_INPUT: 422,
            ErrorCodes.INVALID_OPERATION: 400,
            ErrorCodes.REQUIRED_AUTHENTICATION: 410,
            ErrorCodes.INTERNAL_SERVER_ERROR: 500,
            ErrorCodes.FILE_SIZE_EXCEEDED: 413,
            ErrorCodes.RATE_LIMIT_EXCEEDED: 429,
        }

        return status_codes.get(self.code, 500)
