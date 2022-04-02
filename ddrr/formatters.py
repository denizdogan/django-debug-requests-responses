import logging

from django.core.management.color import supports_color
from django.template import Context
from django.template import RequestContext
from django.template import Template
from django.template.loader import get_template

from ddrr.records import RequestLogRecord
from ddrr.records import ResponseLogRecord


class DjangoTemplateRequestFormatter(logging.Formatter):
    # noinspection PyMissingConstructor
    def __init__(
        self,
        *,
        template_name=None,
        template=None,
        pretty=False,
        limit_body=None,
        colors=True,
    ):
        if not template_name and not template:
            raise RuntimeError(
                "DjangoTemplateRequestFormatter requires a template_name or "
                "template setting"
            )
        self._template_name = template_name
        self._template = template
        self.pretty = pretty
        self.limit_body = limit_body
        self.colors = colors and supports_color()

    @property
    def template(self):
        # lazy loading of template to avoid AppRegistryNotReady
        return (
            # circumvent autoescape being forced onto the template context by
            # extracting the source and creating a separate Template object
            Template(get_template(self._template_name).template.source)
            if self._template_name
            else Template(self._template)
        )

    def format(self, record):
        ddrr = RequestLogRecord.make(record, self)
        ctx = RequestContext(
            request=record.msg,
            dict_={"ddrr": ddrr, "record": record, "formatter": self},
            autoescape=False,
        )
        # noinspection PyBroadException
        try:
            return self.template.render(ctx)
        except:  # noqa: E722
            return "<template failed to render>"


class DjangoTemplateResponseFormatter(logging.Formatter):
    # noinspection PyMissingConstructor
    def __init__(
        self,
        *,
        template_name=None,
        template=None,
        pretty=False,
        limit_body=None,
        colors=True,
    ):
        if not template_name and not template:
            raise RuntimeError(
                "DjangoTemplateResponseFormatter requires a template_name or "
                "template setting"
            )
        self._template_name = template_name
        self._template = template
        self.pretty = pretty
        self.limit_body = limit_body
        self.colors = colors and supports_color()

    @property
    def template(self):
        # lazy loading of template to avoid AppRegistryNotReady
        return (
            # circumvent autoescape being forced onto the template context by
            # extracting the source and creating a separate Template object
            Template(get_template(self._template_name).template.source)
            if self._template_name
            else Template(self._template)
        )

    def format(self, record):
        ddrr = ResponseLogRecord.make(record, self)
        ctx = Context(
            dict_={"ddrr": ddrr, "record": record, "formatter": self},
            autoescape=False,
        )
        # noinspection PyBroadException
        try:
            return self.template.render(ctx)
        except:  # noqa: E722
            return "<template failed to render>"
