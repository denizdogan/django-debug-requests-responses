import json
import re
import textwrap
from collections import OrderedDict
from xml.dom import minidom

import attr
from django.utils.functional import cached_property

from ddrr.helpers import collect_request_headers

try:
    from lxml import etree
    from lxml.etree import XMLSyntaxError
except ImportError:
    etree = None
    XMLSyntaxError = None


def pretty_print_json(content):
    """
    Pretty-print a JSON string and return it.

    >>> pretty_print_json('')
    ''
    >>> pretty_print_json('foobar')
    'foobar'
    >>> pretty_print_json('{"foo":"bar"}')
    '{\\n  "foo": "bar"\\n}'
    >>> pretty_print_json('   {"foo"  : "bar"  }')
    '{\\n  "foo": "bar"\\n}'

    :param content: JSON string
    :return: Pretty-printed JSON string
    """
    try:
        data = json.loads(content)
        return json.dumps(data, indent=2)
    except json.decoder.JSONDecodeError:
        return content


def pretty_print_xml(content):
    """
    Pretty-print an XML string and return it.

    >>> pretty_print_xml('')
    ''
    >>> pretty_print_xml('<p></u>')
    '<p></u>'
    >>> pretty_print_xml('<p><div><b>hel</b>lo!</div></p>')
    '<p>\\n  <div><b>hel</b>lo!</div>\\n</p>\\n'

    :param content: XML string
    :return: Pretty-printed XML string
    """
    if etree:
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.fromstring(content, parser)
            return etree.tostring(tree, encoding=str, pretty_print=True)
        except XMLSyntaxError:
            return content
    # noinspection PyBroadException
    try:
        return minidom.parseString(content).toprettyxml(indent="  ")
    except Exception:
        return content


PRETTY_PRINTERS = OrderedDict(
    ((r"/json", pretty_print_json), (r"/xml", pretty_print_xml))
)


def pretty_print(content, content_type):
    for regex, handler in PRETTY_PRINTERS.items():
        if re.search(regex, content_type):
            return handler(content)
    return content


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
        if self._formatter.pretty:
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
