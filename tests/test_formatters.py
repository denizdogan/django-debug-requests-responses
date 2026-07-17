import logging

import pytest
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.test import RequestFactory

from ddrr.formatters import DjangoTemplateRequestFormatter
from ddrr.formatters import DjangoTemplateResponseFormatter


def test_django_template_formatter_no_template():
    """
    Passing neither `template` nor `template_name` to DjangoTemplateRequestFormatter
    raises RuntimeError.
    """
    with pytest.raises(RuntimeError):
        DjangoTemplateRequestFormatter()


def test_django_template_formatter_template_name():
    """
    Passing `template_name` to DjangoTemplateRequestFormatter raises no exceptions.
    """
    DjangoTemplateRequestFormatter(template_name="template_name.html")


def test_django_template_formatter_template_string():
    """
    Passing `template` to DjangoTemplateRequestFormatter raises no errors.
    """
    DjangoTemplateRequestFormatter(template="{{ foo }}")


def test_django_template_lazy_loading():
    """
    Template resolution in DjangoTemplateRequestFormatter is not performed until
    accessing the `template` property.
    """
    formatter = DjangoTemplateRequestFormatter(template_name="template_name.html")
    with pytest.raises(TemplateDoesNotExist):
        # noinspection PyStatementEffect
        formatter.template


def test_django_template_request_formatter_handles_consumed_body():
    request = RequestFactory().post("/", {"field": "value"})
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
    formatter = DjangoTemplateRequestFormatter(template="{{ ddrr.body }}", colors=False)

    assert formatter.format(record) == "<request body unavailable: already read>"


def test_default_request_template_uses_directional_header():
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
    formatter = DjangoTemplateRequestFormatter(
        template_name="ddrr/default-request.html", colors=False
    )

    output = formatter.format(record)

    assert output.startswith("← GET /widgets?active=true\n")
    assert "  Accept: text/plain\n" in output
    assert output.endswith("  Accept: text/plain\n")


def test_default_response_template_uses_directional_header():
    response = HttpResponse(b"Created", status=201, content_type="text/plain")
    record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg=response,
        args=(),
        exc_info=None,
    )
    formatter = DjangoTemplateResponseFormatter(
        template_name="ddrr/default-response.html", colors=False
    )

    output = formatter.format(record)

    assert output.startswith("→ 201 Created\n")
    assert "  Content-Type: text/plain\n" in output
    assert output.endswith("\nCreated\n")
