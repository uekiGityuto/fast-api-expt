import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

logger = logging.getLogger()


def generate_request_id():
    return str(uuid.uuid4())


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = generate_request_id()
        start_time = time.time()
        request.state.request_id = request_id

        response = await call_next(request)

        duration = time.time() - start_time
        log = {
            "request": {
                "id": request_id,
                "uri": request.url.path,
                "headers": dict(request.headers),
                "method": request.method,
            },
            "response": {
                "status": response.status_code,
                "duration": duration,
            },
        }
        logger.info(log)

        return response
