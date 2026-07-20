import logging

from django.http import HttpResponse
from django.test import RequestFactory

from ddrr.formatters import RequestFormatter
from ddrr.formatters import ResponseFormatter


def test_request_formatter_handles_consumed_body():
    request = RequestFactory().post("/", {"field": "value"})

    # "read" the request body
    assert request.POST["field"] == "value"

    record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg=request,
        args=(),
        exc_info=None,
    )
    formatter = RequestFormatter(colors=False)

    assert "<request body unavailable: already read>" in formatter.format(record)


def test_request_formatter_uses_directional_header():
    request = RequestFactory().get("/widgets?active=true", HTTP_ACCEPT="text/plain")
    record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg=request,
        args=(),
        exc_info=None,
    )
    formatter = RequestFormatter(colors=False)

    output = formatter.format(record)

    assert output.startswith("← GET /widgets?active=true\n")
    assert "  Accept: text/plain\n" in output
    assert output.endswith("  Accept: text/plain\n")


def test_response_formatter_uses_directional_header():
    response = HttpResponse(b"Created", status=201, content_type="text/plain")
    response.set_cookie("sessionid", "abc", httponly=True)
    response.set_cookie("theme", "dark")
    record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg=response,
        args=(),
        exc_info=None,
    )
    formatter = ResponseFormatter(colors=False)

    output = formatter.format(record)

    assert output.startswith("→ 201 Created\n")
    assert "  Content-Type: text/plain\n" in output
    assert f"  Set-Cookie: {response.cookies['sessionid'].OutputString()}\n" in output
    assert f"  Set-Cookie: {response.cookies['theme'].OutputString()}\n" in output
    assert output.endswith("\nCreated\n")
