from enum import Enum

from fastapi import HTTPException


class ErrorDetail(Enum):
    LOGIN_FAILURE = "LOGIN_FAILURE"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INACTIVE_USER = "INACTIVE_USER"
    UNAUTHORIZED_OPERATION = "UNAUTHORIZED_OPERATION"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"


def raise_http_exception(status_code: int, detail: ErrorDetail, headers: dict | None = None):
    raise HTTPException(status_code=status_code,
                        detail=detail.value, headers=headers)
