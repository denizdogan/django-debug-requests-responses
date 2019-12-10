import textwrap

import attr
from django.utils.functional import cached_property

from ddrr.utils import collect_request_headers
from ddrr.utils import pretty_print


@attr.s
class RequestLogRecord:
    record = attr.ib()
    request = attr.ib()
    _formatter = attr.ib()

    @cached_property
    def headers(self):
        return collect_request_headers(self.request)

    @cached_property
    def body(self):
        try:
            content = self.request.body.decode("utf-8")
        except UnicodeDecodeError:
            content = str(self.request.body)
        # optionally pretty print
        if self._formatter.pretty:
            content = pretty_print(content, self.content_type)
        # optionally limit output
        if self._formatter.limit_body:
            content = textwrap.shorten(
                content, self._formatter.limit_body, placeholder="..."
            )
        return content

    @cached_property
    def method(self):
        return self.request.method

    @cached_property
    def path(self):
        return self.request.path

    @cached_property
    def query_string(self):
        query_params = self.query_params
        if not len(query_params):
            return ""
        return "?" + query_params.urlencode()

    @cached_property
    def query_params(self):
        return self.request.GET

    @cached_property
    def content_type(self):
        return self.headers.get("Content-Type", "")

    @classmethod
    def make(cls, record, formatter):
        return cls(record=record, request=record.msg, formatter=formatter)


@attr.s
class ResponseLogRecord:
    record = attr.ib()
    response = attr.ib()
    _formatter = attr.ib()

    @cached_property
    def headers(self):
        return dict(self.response.items())

    @cached_property
    def reason_phrase(self):
        return self.response.reason_phrase

    @cached_property
    def status_code(self):
        return self.response.status_code

    @cached_property
    def content(self):
        try:
            if self.response.streaming:
                content = "<streaming>"
            else:
                content = self.response.content.decode("utf-8")
        except UnicodeDecodeError:
            content = str(self.response.content)
        # optionally pretty print
        if self.content_type and self._formatter.pretty:
            content = pretty_print(content, self.content_type)
        # optionally limit output
        if self._formatter.limit_body:
            content = textwrap.shorten(
                content, self._formatter.limit_body, placeholder="..."
            )
        return content

    @cached_property
    def content_type(self):
        return self.headers.get("Content-Type")

    @classmethod
    def make(cls, record, formatter):
        return cls(record=record, response=record.msg, formatter=formatter)
