from enum import Enum


class ErrorCodes(Enum):
    UNAUTHORIZED = "UNAUTHORIZED"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    MESSAGE_SAVE_ERROR = "MESSAGE_SAVE_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_OPERATION = "INVALID_OPERATION"
    INVALID_STATE = "INVALID_STATE"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    FILE_SIZE_EXCEEDED = "FILE_SIZE_EXCEEDED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"


class ExceptionHandler(Exception):
    def __init__(self, code: ErrorCodes, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(msg)

    def statusCode(self) -> int:
        status_codes = {
            ErrorCodes.UNAUTHORIZED: 401,
            ErrorCodes.ALREADY_EXISTS: 409,
            ErrorCodes.MESSAGE_SAVE_ERROR: 500,
            ErrorCodes.NOT_FOUND: 404,
            ErrorCodes.INVALID_PAYLOAD: 400,
            ErrorCodes.INVALID_INPUT: 422,
            ErrorCodes.INVALID_OPERATION: 400,
            ErrorCodes.INVALID_STATE: 400,
            ErrorCodes.FORBIDDEN: 403,
            ErrorCodes.CONFLICT: 409,
            ErrorCodes.INTERNAL_SERVER_ERROR: 500,
            ErrorCodes.BAD_REQUEST: 400,
            ErrorCodes.FILE_SIZE_EXCEEDED: 413,
            ErrorCodes.RATE_LIMIT_EXCEEDED: 429,
        }

        return status_codes.get(self.code, 500)
