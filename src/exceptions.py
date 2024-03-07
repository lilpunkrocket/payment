from fastapi.responses import PlainTextResponse
from logger.core import log_error


async def http_exception_handler(request, exc):
    log_dict = {
        'user': request.client.host,
        'method': request.method,
        'path': request.url,
        'status_code': exc.status_code,
        'detail': str(exc.detail),
    }

    await log_error(**log_dict)

    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
