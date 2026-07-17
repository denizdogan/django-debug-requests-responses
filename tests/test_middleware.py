from unittest.mock import Mock

import pytest
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse

from ddrr.middleware import DebugRequestsResponses


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
    assert request_logger.debug.call_count == request_calls
    assert response_logger.debug.call_count == response_calls
