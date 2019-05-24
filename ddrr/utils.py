import logging

from django.conf import settings

from ddrr.formatters import DjangoTemplateRequestFormatter
from ddrr.formatters import DjangoTemplateResponseFormatter
from ddrr.loggers import request_logger
from ddrr.loggers import response_logger


def quick_setup(
    enable_requests=True,
    enable_responses=True,
    level="DEBUG",
    pretty=False,
    request_template_name="ddrr/default-request.html",
    request_template=None,
    response_template_name="ddrr/default-response.html",
    response_template=None,
    request_handler=logging.StreamHandler(),
    response_handler=logging.StreamHandler(),
    colors=True,
    limit_body=None,
):
    """
    Set up DDRR logging.

    :param enable_requests: Enable request logging
    :param enable_responses: Enable response logging
    :param level: Log level
    :param pretty: Pretty-print bodies
    :param request_template_name: Request template name
    :param request_template: Request template string
    :param response_template_name: Response template name
    :param response_template: Response template string
    :param request_handler: Custom request handler
    :param response_handler: Custom response handler
    :param colors: Use colors if available
    :param limit_body: Limit request and response body
    """
    # set up middleware
    if "ddrr.middleware.DebugRequestsResponses" not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.insert(0, "ddrr.middleware.DebugRequestsResponses")

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
