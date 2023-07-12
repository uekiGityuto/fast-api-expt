from enum import Enum


class ErrorDetail(Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"


class DomainException(Exception):
    def __init__(self, detail: ErrorDetail):
        self.detail = detail.value
