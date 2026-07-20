import logging

from django.core.management.color import supports_color
from django.utils.termcolors import colorize

from ddrr.records import RequestLogRecord
from ddrr.records import ResponseLogRecord


# C0 and C1 are the character ranges terminals interpret as controls.
_CONTROL_ESCAPES = {
    code: f"\\x{code:02x}" for code in (*range(0x00, 0x20), *range(0x7F, 0xA0))
}
_CONTROL_ESCAPES.update({ord("\t"): r"\t", ord("\n"): r"\n", ord("\r"): r"\r"})
_BODY_CONTROL_ESCAPES = {
    code: escape for code, escape in _CONTROL_ESCAPES.items() if code != ord("\n")
}


def _escape_controls(value):
    return str(value).translate(_CONTROL_ESCAPES)


def _escape_body_controls(value):
    return str(value).translate(_BODY_CONTROL_ESCAPES)


def _format_message(start_line, headers, body):
    lines = [start_line]
    for name, value in headers:
        lines.append(f"  {_escape_controls(name)}: {_escape_controls(value)}")
    if body:
        lines.append("")
        body = _escape_body_controls(body)
        lines.append("  " + body.replace("\n", "\n  "))
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
            method = _escape_controls(request.method)
            target = _escape_controls(f"{request.path}{request.query_string}")
            return _format_message(
                f"{marker} {method} {target}",
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
            status = _escape_controls(response.status_code)
            reason = _escape_controls(response.reason_phrase)
            return _format_message(
                f"{marker} {status} {reason}",
                response.header_items,
                response.content,
            )
        except Exception:
            return "<response failed to format>"
