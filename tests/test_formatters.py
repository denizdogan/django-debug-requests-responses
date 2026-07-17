import logging

import pytest
from django.template import TemplateDoesNotExist
from django.test import RequestFactory

from ddrr.formatters import DjangoTemplateRequestFormatter


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
