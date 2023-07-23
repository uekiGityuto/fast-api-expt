import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

logger = logging.getLogger('uvicorn')


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next: RequestResponseEndpoint) -> Response:
        if req.url.path == "/health":
            return await call_next(req)

        start_time = time.time()
        request_id = str(uuid.uuid4())
        req.state.request_id = request_id

        response = await call_next(req)

        duration = time.time() - start_time
        log = {
            "request": {
                "id": request_id,
                "uri": req.url.path,
                "headers": dict(req.headers),
                "method": req.method,
            },
            "response": {
                "status": response.status_code,
                "duration": duration,
            },
        }
        logger.info(log)

        return response
