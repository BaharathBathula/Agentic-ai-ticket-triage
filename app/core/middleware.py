import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


logger = logging.getLogger("api.request")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Adds a request ID and logs request duration.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid4()),
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "request_failed request_id=%s method=%s path=%s",
                request_id,
                request.method,
                request.url.path,
            )
            raise

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            (
                "request_complete request_id=%s method=%s "
                "path=%s status=%s duration_ms=%s"
            ),
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
