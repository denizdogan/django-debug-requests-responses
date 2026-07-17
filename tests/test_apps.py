import logging

import ddrr
import pytest

from ddrr.apps import DDRRConfig


@pytest.mark.parametrize(
    ("enable_requests", "enable_responses"),
    [
        (False, True),
        (True, False),
    ],
)
def test_ready_only_adds_enabled_handlers(
    settings, monkeypatch, enable_requests, enable_responses
):
    request_handler = logging.NullHandler()
    response_handler = logging.NullHandler()
    settings.DDRR = {
        "ENABLE_REQUESTS": enable_requests,
        "ENABLE_RESPONSES": enable_responses,
        "REQUEST_HANDLER": request_handler,
        "RESPONSE_HANDLER": response_handler,
    }
    request_logger = logging.Logger("test-ddrr-request-logger")
    response_logger = logging.Logger("test-ddrr-response-logger")
    monkeypatch.setattr("ddrr.apps.request_logger", request_logger)
    monkeypatch.setattr("ddrr.apps.response_logger", response_logger)

    DDRRConfig("ddrr", ddrr).ready()

    assert request_logger.handlers == ([request_handler] if enable_requests else [])
    assert response_logger.handlers == ([response_handler] if enable_responses else [])


def test_disable_django_server_log_survives_logger_being_reenabled(
    settings, monkeypatch
):
    settings.DDRR = {
        "DISABLE_DJANGO_SERVER_LOG": True,
        "REQUEST_HANDLER": logging.NullHandler(),
        "RESPONSE_HANDLER": logging.NullHandler(),
    }
    request_logger = logging.Logger("test-ddrr-request-logger")
    response_logger = logging.Logger("test-ddrr-response-logger")
    django_server_logger = logging.Logger("django.server")
    get_logger = logging.getLogger
    monkeypatch.setattr("ddrr.apps.request_logger", request_logger)
    monkeypatch.setattr("ddrr.apps.response_logger", response_logger)
    monkeypatch.setattr(
        "ddrr.apps.logging.getLogger",
        lambda name=None: (
            django_server_logger if name == "django.server" else get_logger(name)
        ),
    )

    DDRRConfig("ddrr", ddrr).ready()
    django_server_logger.disabled = False

    record = logging.LogRecord(
        name="django.server",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="request",
        args=(),
        exc_info=None,
    )
    assert not django_server_logger.filter(record)
