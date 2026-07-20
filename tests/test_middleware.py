import asyncio
import logging
from logging.handlers import BufferingHandler
from unittest.mock import Mock

import ddrr
import pytest
from asgiref.sync import iscoroutinefunction
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse

from ddrr.apps import DDRRConfig
from ddrr.middleware import DebugRequestsResponses


def test_async_request_and_response_are_logged(settings, monkeypatch):
    settings.DDRR = {}
    request = HttpRequest()
    response = HttpResponse()
    events = []

    async def get_response(received_request):
        events.append(("view", received_request))
        return response

    request_logger = Mock()
    response_logger = Mock()
    request_logger.getEffectiveLevel.return_value = logging.DEBUG
    response_logger.getEffectiveLevel.return_value = logging.DEBUG
    request_logger.log.side_effect = lambda level, value: events.append(
        ("request", level, value)
    )
    response_logger.log.side_effect = lambda level, value: events.append(
        ("response", level, value)
    )
    monkeypatch.setattr("ddrr.middleware.request_logger", request_logger)
    monkeypatch.setattr("ddrr.middleware.response_logger", response_logger)

    middleware = DebugRequestsResponses(get_response)

    assert getattr(DebugRequestsResponses, "sync_capable") is True
    assert getattr(DebugRequestsResponses, "async_capable") is True
    assert iscoroutinefunction(middleware)
    assert asyncio.run(middleware(request)) is response
    assert events == [
        ("request", logging.DEBUG, request),
        ("view", request),
        ("response", logging.DEBUG, response),
    ]


def test_logging_uses_configured_level(settings, monkeypatch):
    handler = BufferingHandler(capacity=2)
    logger = logging.Logger("test-ddrr-request", level=logging.DEBUG)
    settings.MIDDLEWARE = ["ddrr.middleware.DebugRequestsResponses"]
    settings.DDRR = {
        "LEVEL": "INFO",
        "ENABLE_RESPONSES": False,
        "REQUEST_HANDLER": handler,
    }
    monkeypatch.setattr("ddrr.apps.request_logger", logger)
    monkeypatch.setattr("ddrr.apps.response_logger", logging.Logger("test-response"))
    monkeypatch.setattr("ddrr.middleware.request_logger", logger)
    DDRRConfig("ddrr", ddrr).ready()
    request = HttpRequest()
    response = HttpResponse()

    middleware = DebugRequestsResponses(Mock(return_value=response))

    assert middleware(request) is response
    assert [(record.levelno, record.msg) for record in handler.buffer] == [
        (logging.INFO, request)
    ]


@pytest.mark.parametrize("failing_logger", ["request_logger", "response_logger"])
def test_logging_failure_does_not_interrupt_request(
    settings, monkeypatch, failing_logger
):
    settings.DDRR = {}
    request = HttpRequest()
    response = HttpResponse()
    get_response = Mock(return_value=response)
    loggers = {
        "request_logger": Mock(),
        "response_logger": Mock(),
    }
    loggers[failing_logger].log.side_effect = RuntimeError("handler failed")
    for name, logger in loggers.items():
        monkeypatch.setattr(f"ddrr.middleware.{name}", logger)

    middleware = DebugRequestsResponses(get_response)

    assert middleware(request) is response
    get_response.assert_called_once_with(request)


def test_request_and_response_are_logged(client, caplog):
    """
    Requests and responses are logged.
    """
    client.get(reverse("index"))
    assert isinstance(caplog.records[0].msg, HttpRequest)
    assert isinstance(caplog.records[1].msg, HttpResponse)
    assert len(caplog.records) == 2


@pytest.mark.parametrize(
    ("ddrr_settings", "request_calls", "response_calls"),
    [
        ({"ENABLE_REQUESTS": False}, 0, 1),
        ({"ENABLE_RESPONSES": False}, 1, 0),
    ],
)
def test_request_or_response_logging_can_be_disabled(
    settings, monkeypatch, ddrr_settings, request_calls, response_calls
):
    settings.DDRR = ddrr_settings
    request = HttpRequest()
    response = HttpResponse()
    get_response = Mock(return_value=response)
    request_logger = Mock()
    response_logger = Mock()
    monkeypatch.setattr("ddrr.middleware.request_logger", request_logger)
    monkeypatch.setattr("ddrr.middleware.response_logger", response_logger)

    middleware = DebugRequestsResponses(get_response)

    assert middleware(request) is response
    get_response.assert_called_once_with(request)
    assert request_logger.log.call_count == request_calls
    assert response_logger.log.call_count == response_calls
