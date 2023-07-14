import logging

from fastapi import HTTPException, Request, status

from app.usecases.errors import AuthException, DomainException, ErrorDetail

logger = logging.getLogger('uvicorn')


def handle_error(e: Exception, req: Request):
    request_id = req.state.request_id if hasattr(req.state, "request_id") else None
    if isinstance(e, AuthException):
        match e.detail:
            case ErrorDetail.INVALID_CREDENTIALS:
                status_code = status.HTTP_401_UNAUTHORIZED
                headers = {"WWW-Authenticate": "Bearer"}
            case _:
                status_code = status.HTTP_403_FORBIDDEN
                headers = None
        logger.warning(e.detail.value, extra={'request_id': request_id})
        raise HTTPException(
            status_code=status_code, detail=e.detail.value, headers=headers)

    if isinstance(e, DomainException):
        match e.detail:
            case ErrorDetail.NOT_FOUND:
                status_code = status.HTTP_404_NOT_FOUND
                headers = None
            case _:
                status_code = status.HTTP_400_BAD_REQUEST
                headers = None
        raise HTTPException(
            status_code=status_code, detail=e.detail.value, headers=headers)

    logger.exception(ErrorDetail.UNEXPECTED_ERROR.value,
                     exc_info=e, extra={'request_id': request_id})
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorDetail.UNEXPECTED_ERROR.value)
