from enum import Enum


class ErrorDetail(Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    LOGIN_FAILED = "LOGIN_FAILED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INACTIVE_USER = "INACTIVE_USER"
    UNAUTHORIZED_OPERATION = "UNAUTHORIZED_OPERATION"


class DomainException(Exception):
    def __init__(self, detail: ErrorDetail):
        self.detail = detail
