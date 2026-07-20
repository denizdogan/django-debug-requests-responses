import logging

from django.core.management.color import supports_color
from django.utils.termcolors import colorize

from ddrr.records import RequestLogRecord
from ddrr.records import ResponseLogRecord


def _format_message(start_line, headers, body):
    lines = [start_line]
    for name, value in headers:
        lines.append(f"  {name}: {value}")
    if body:
        lines.append("")
        lines.append(body)
    return "\n".join(lines) + "\n"


class RequestFormatter(logging.Formatter):
    def __init__(self, *, pretty=False, limit_body=None, colors=True):
        super().__init__()
        self.pretty = pretty
        self.limit_body = limit_body
        self.colors = colors and supports_color()

    def format(self, record):
        try:
            request = RequestLogRecord.make(record, self)
            marker = colorize("←", fg="cyan") if self.colors else "←"
            return _format_message(
                f"{marker} {request.method} {request.path}{request.query_string}",
                request.headers.items(),
                request.body,
            )
        except Exception:
            return "<request failed to format>"


class ResponseFormatter(logging.Formatter):
    def __init__(self, *, pretty=False, limit_body=None, colors=True):
        super().__init__()
        self.pretty = pretty
        self.limit_body = limit_body
        self.colors = colors and supports_color()

    def format(self, record):
        try:
            response = ResponseLogRecord.make(record, self)
            marker = colorize("→", fg="magenta") if self.colors else "→"
            return _format_message(
                f"{marker} {response.status_code} {response.reason_phrase}",
                response.header_items,
                response.content,
            )
        except Exception:
            return "<response failed to format>"
