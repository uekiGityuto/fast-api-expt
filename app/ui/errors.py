from fastapi import HTTPException, status

from app.usecases.errors import DomainException, ErrorDetail


def handle_error(e: Exception):
    # TODO: ロギング
    if isinstance(e, DomainException):
        match e.detail:
            case ErrorDetail.NOT_FOUND:
                status_code = status.HTTP_404_NOT_FOUND
                headers = None
            case ErrorDetail.LOGIN_FAILED | ErrorDetail.UNAUTHORIZED_OPERATION:
                status_code = status.HTTP_403_FORBIDDEN
                headers = None
            case ErrorDetail.INVALID_CREDENTIALS:
                status_code = status.HTTP_401_UNAUTHORIZED
                headers = {"WWW-Authenticate": "Bearer"}
            case _:
                status_code = status.HTTP_400_BAD_REQUEST
                headers = None
        raise HTTPException(
            status_code=status_code, detail=e.detail.value, headers=headers)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='UNEXPECTED_ERROR')
