from enum import Enum

from fastapi import HTTPException, status

from app.usecases.errors import DomainException, ErrorDetail


class ErrorDetail2(Enum):
    LOGIN_FAILURE = "LOGIN_FAILURE"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INACTIVE_USER = "INACTIVE_USER"
    UNAUTHORIZED_OPERATION = "UNAUTHORIZED_OPERATION"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"


def raise_http_exception(status_code: int, detail: ErrorDetail2, headers: dict | None = None):
    raise HTTPException(status_code=status_code,
                        detail=detail.value, headers=headers)


def handle_error(e: Exception):
    # TODO: ロギング
    if isinstance(e, DomainException):
        match e.detail:
            case ErrorDetail.NOT_FOUND:
                status_code = status.HTTP_404_NOT_FOUND
            case ErrorDetail.AUTHENTICATION_FAILED:
                status_code = status.HTTP_403_FORBIDDEN
            case _:
                status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status_code, detail=e.detail)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='UNEXPECTED_ERROR')
