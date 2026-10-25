from asgiref.sync import iscoroutinefunction
from django.conf import settings
from django.utils.decorators import sync_and_async_middleware

from ddrr.loggers import request_logger, response_logger


def _log_safely(logger, value):
    try:
        logger.log(logger.getEffectiveLevel(), value)
    except Exception:  # noqa: BLE001, S110 - Do not log a logging failure.
        pass


@sync_and_async_middleware
def DebugRequestsResponses(get_response):
    config = getattr(settings, "DDRR", None) or {}
    enable_requests = config.get("ENABLE_REQUESTS", True)
    enable_responses = config.get("ENABLE_RESPONSES", True)

    # Keep asgiref's Python 3.11 coroutine-marker support; ty sees its old fallback.
    if iscoroutinefunction(get_response):  # ty: ignore[deprecated]

        async def middleware(request):
            if enable_requests:
                _log_safely(request_logger, request)
            response = await get_response(request)
            if enable_responses:
                _log_safely(response_logger, response)
            return response

    else:

        def middleware(request):
            if enable_requests:
                _log_safely(request_logger, request)
            response = get_response(request)
            if enable_responses:
                _log_safely(response_logger, response)
            return response

    return middleware
