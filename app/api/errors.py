from enum import Enum

from fastapi import HTTPException, status

from app.usecases.errors import DomainException


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


def handle_error(e: Exception):
    # TODO: ロギング
    if isinstance(e, DomainException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='UNEXPECTED_ERROR')
