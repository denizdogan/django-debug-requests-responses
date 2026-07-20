import logging

from django.http import HttpResponse
from django.test import RequestFactory

from ddrr.formatters import RequestFormatter
from ddrr.formatters import ResponseFormatter


def make_record(message):
    return logging.makeLogRecord({"msg": message})


def test_request_formatter_handles_consumed_body():
    request = RequestFactory().post("/", {"field": "value"})

    # "read" the request body
    assert request.POST["field"] == "value"

    formatter = RequestFormatter(colors=False)

    assert "<request body unavailable: already read>" in formatter.format(
        make_record(request)
    )


def test_request_formatter_uses_ascii_marker_and_unindented_headers():
    request = RequestFactory().get("/widgets?active=true", HTTP_ACCEPT="text/plain")
    formatter = RequestFormatter(colors=False)

    output = formatter.format(make_record(request))

    assert output.startswith("<- GET /widgets?active=true\n")
    assert "Accept: text/plain\n" in output
    assert output.endswith("Accept: text/plain\n")


def test_response_formatter_uses_ascii_marker_and_unindented_output():
    response = HttpResponse(b"Created", status=201, content_type="text/plain")
    response.set_cookie("sessionid", "abc", httponly=True)
    response.set_cookie("theme", "dark")
    formatter = ResponseFormatter(colors=False)

    output = formatter.format(make_record(response))

    assert output.startswith("-> 201 Created\n")
    assert "Content-Type: text/plain\n" in output
    assert f"Set-Cookie: {response.cookies['sessionid'].OutputString()}\n" in output
    assert f"Set-Cookie: {response.cookies['theme'].OutputString()}\n" in output
    assert output.endswith("\nCreated\n")


def test_request_formatter_escapes_control_characters():
    request = RequestFactory().get("/", HTTP_X_UNTRUSTED="value\r\n-> forged\x1b[2J")
    request.path = "/safe\n-> forged\x1b[2J"

    output = RequestFormatter(colors=False).format(make_record(request))

    assert output.startswith("<- GET /safe\\n-> forged\\x1b[2J\n")
    assert "X-Untrusted: value\\r\\n-> forged\\x1b[2J\n" in output
    assert "\x1b" not in output
    assert "\n-> forged" not in output


def test_response_formatter_preserves_body_indentation_and_escapes_markers():
    response = HttpResponse(
        "first\n  indented\n-> forged\x1b[2J", content_type="text/plain"
    )

    output = ResponseFormatter(colors=False).format(make_record(response))

    assert output.endswith("\n\nfirst\n  indented\n\\-> forged\\x1b[2J\n")
    assert "\x1b" not in output
