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


class ExceptionHandler(Exception):
    def __init__(self, code: ErrorCodes, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(msg)
