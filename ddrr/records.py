import json

import attr
from django.utils.functional import cached_property

from ddrr.utils import collect_request_headers
from ddrr.utils import collect_response_headers


@attr.s
class RequestLogRecord(object):
    record = attr.ib()
    request = attr.ib()
    _formatter = attr.ib()

    @cached_property
    def headers(self):
        return collect_request_headers(self.request)

    @cached_property
    def body(self):
        content = self.request.body.decode("utf-8")
        # optionally pretty print
        if self._formatter.pretty and "/json" in self.content_type:
            # noinspection PyBroadException
            try:
                data = json.loads(content)
                content = json.dumps(data, indent=2)
            except Exception:
                pass
        # optionally limit output
        limit = self._formatter.limit_body
        if limit and len(content) > limit:
            content = content[:limit] + "..."
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
class ResponseLogRecord(object):
    record = attr.ib()
    response = attr.ib()
    _formatter = attr.ib()

    @cached_property
    def headers(self):
        return collect_response_headers(self.response)

    @cached_property
    def reason_phrase(self):
        return self.response.reason_phrase

    @cached_property
    def status_code(self):
        return self.response.status_code

    @cached_property
    def content(self):
        content = self.response.content.decode("utf-8")
        if self._formatter.pretty and "/json" in self.content_type:
            # noinspection PyBroadException
            try:
                data = json.loads(content)
                return json.dumps(data, indent=2)
            except Exception:
                pass
        return content

    @cached_property
    def method(self):
        return self.response.method

    @cached_property
    def content_type(self):
        return self.headers.get("Content-Type")

    @classmethod
    def make(cls, record, formatter):
        return cls(record=record, response=record.msg, formatter=formatter)
