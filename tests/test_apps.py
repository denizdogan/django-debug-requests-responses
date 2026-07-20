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
