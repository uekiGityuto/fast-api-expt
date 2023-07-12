from enum import Enum


class ErrorDetail(Enum):
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"


class DomainException(Exception):
    def __init__(self, detail: ErrorDetail):
        self.detail = detail.value
