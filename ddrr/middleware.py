from django.conf import settings

from ddrr.loggers import request_logger
from ddrr.loggers import response_logger


def _log_safely(logger, value):
    try:
        logger.log(logger.getEffectiveLevel(), value)
    except Exception:
        pass


class DebugRequestsResponses:
    def __init__(self, get_response):
        self.get_response = get_response
        config = getattr(settings, "DDRR", None) or {}
        self.enable_requests = config.get("ENABLE_REQUESTS", True)
        self.enable_responses = config.get("ENABLE_RESPONSES", True)

    def __call__(self, request):
        if self.enable_requests:
            _log_safely(request_logger, request)
        response = self.get_response(request)
        if self.enable_responses:
            _log_safely(response_logger, response)
        return response
