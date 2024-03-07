from fastapi import Request
from logger.core import log_info
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        response = await call_next(request)

        log_dict = {
            'user': request.client.host,
            'method': request.method,
            'path': request.url,
            'status_code': response.status_code,
        }

        await log_info(**log_dict)

        return response
