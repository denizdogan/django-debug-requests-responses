import logging

from django.apps import AppConfig
from django.conf import settings

from ddrr.formatters import DjangoTemplateRequestFormatter
from ddrr.formatters import DjangoTemplateResponseFormatter
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
        request_template_name = s(
            "REQUEST_TEMPLATE_NAME", "ddrr/default-request.html"
        )
        request_template = s("REQUEST_TEMPLATE", None)
        response_template_name = s(
            "RESPONSE_TEMPLATE_NAME", "ddrr/default-response.html"
        )
        response_template = s("RESPONSE_TEMPLATE", None)
        request_handler = s("REQUEST_HANDLER", logging.StreamHandler())
        response_handler = s("RESPONSE_HANDLER", logging.StreamHandler())
        colors = s("ENABLE_COLORS", True)
        limit_body = s("LIMIT_BODY", None)
        disable_django_server_log = s("DISABLE_DJANGO_SERVER_LOG", False)

        # set up request logger and handler
        request_handler.setLevel(level)
        request_logger.setLevel(level)
        request_logger.addHandler(request_handler)
        if not enable_requests:
            request_logger.disabled = False

        # set up response logger and handler
        response_handler.setLevel(level)
        response_logger.setLevel(level)
        response_logger.addHandler(response_handler)
        if not enable_responses:
            response_logger.disabled = False

        # set up request formatter
        request_formatter_kwargs = {
            "pretty": pretty,
            "colors": colors,
            "limit_body": limit_body,
        }
        if request_template:
            request_formatter_kwargs["template"] = request_template
        else:
            request_formatter_kwargs["template_name"] = request_template_name
        request_formatter = DjangoTemplateRequestFormatter(
            **request_formatter_kwargs
        )
        request_handler.setFormatter(request_formatter)

        # set up response formatter
        response_formatter_kwargs = {
            "pretty": pretty,
            "colors": colors,
            "limit_body": limit_body,
        }
        if response_template:
            response_formatter_kwargs["template"] = response_template
        else:
            response_formatter_kwargs["template_name"] = response_template_name
        response_formatter = DjangoTemplateResponseFormatter(
            **response_formatter_kwargs
        )
        response_handler.setFormatter(response_formatter)

        # disable django server log
        if disable_django_server_log:
            logging.getLogger("django.server").disabled = True
