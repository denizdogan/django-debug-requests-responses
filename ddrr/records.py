import textwrap
from dataclasses import dataclass
from typing import Any

from django.http import RawPostDataException
from django.utils.functional import cached_property

from ddrr.utils import pretty_print


@dataclass(init=False)
class RequestLogRecord:
    record: Any
    request: Any
    _formatter: Any

    def __init__(self, record: Any, request: Any, formatter: Any) -> None:
        self.record = record
        self.request = request
        self._formatter = formatter

    @cached_property
    def headers(self):
        return self.request.headers

    @cached_property
    def body(self):
        try:
            body = self.request.body
        except RawPostDataException:
            content = "<request body unavailable: already read>"
        else:
            try:
                content = body.decode("utf-8")
            except UnicodeDecodeError:
                content = str(body)
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
        query_string = self.request.META.get("QUERY_STRING", "")
        return f"?{query_string}" if query_string else ""

    @cached_property
    def query_params(self):
        return self.request.GET

    @cached_property
    def content_type(self):
        return self.headers.get("Content-Type", "")

    @classmethod
    def make(cls, record, formatter):
        return cls(record=record, request=record.msg, formatter=formatter)


@dataclass(init=False)
class ResponseLogRecord:
    record: Any
    response: Any
    _formatter: Any

    def __init__(self, record: Any, response: Any, formatter: Any) -> None:
        self.record = record
        self.response = response
        self._formatter = formatter

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
