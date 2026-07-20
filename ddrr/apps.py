import logging

from django.apps import AppConfig
from django.conf import settings

from ddrr.formatters import RequestFormatter
from ddrr.formatters import ResponseFormatter
from ddrr.loggers import request_logger
from ddrr.loggers import response_logger

logger = logging.getLogger(__name__)


class DDRRConfig(AppConfig):
    name = "ddrr"

    def ready(self):
        if "ddrr.middleware.DebugRequestsResponses" not in settings.MIDDLEWARE:
            logger.warning("DDRR middleware not configured")
            return

        def s(name, default):
            config = getattr(settings, "DDRR", None)
            if not config:
                return default
            return config.get(name, default)

        # get settings
        enable_requests = s("ENABLE_REQUESTS", True)
        enable_responses = s("ENABLE_RESPONSES", True)
        level = s("LEVEL", "DEBUG")
        pretty = s("PRETTY_PRINT", False)
        request_handler = s("REQUEST_HANDLER", logging.StreamHandler())
        response_handler = s("RESPONSE_HANDLER", logging.StreamHandler())
        colors = s("ENABLE_COLORS", True)
        limit_body = s("LIMIT_BODY", None)

        # set up request logger and handler
        request_logger.handlers.clear()
        request_logger.propagate = False
        request_handler.setLevel(level)
        request_logger.setLevel(level)
        if enable_requests:
            request_logger.addHandler(request_handler)

        # set up response logger and handler
        response_logger.handlers.clear()
        response_logger.propagate = False
        response_handler.setLevel(level)
        response_logger.setLevel(level)
        if enable_responses:
            response_logger.addHandler(response_handler)

        request_handler.setFormatter(
            RequestFormatter(pretty=pretty, colors=colors, limit_body=limit_body)
        )
        response_handler.setFormatter(
            ResponseFormatter(pretty=pretty, colors=colors, limit_body=limit_body)
        )
