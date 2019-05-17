import pytest
from django.template import TemplateDoesNotExist

from ddrr.formatters import DEFAULT_REQUEST_TEMPLATE
from ddrr.formatters import DefaultRequestFormatter
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


def test_default_request_formatter_template_name():
    """
    Calling DefaultRequestFormatter with no arguments sets `_template_name` to
    DEFAULT_REQUEST_TEMPLATE.
    """
    formatter = DefaultRequestFormatter()
    assert formatter._template_name == DEFAULT_REQUEST_TEMPLATE
