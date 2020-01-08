import json
import re
from collections import OrderedDict
from xml.dom import minidom

import django

try:
    from lxml import etree
    from lxml.etree import XMLSyntaxError
except ImportError:
    etree = None
    XMLSyntaxError = None

KNOWN_HEADERS = {
    "content-md5": "Content-MD5",
    "dnt": "DNT",
    "etag": "ETag",
    "http2-settings": "HTTP2-Settings",
    "im": "IM",
    "p3p": "P3P",
    "te": "TE",
    "www-authenticate": "WWW-Authenticate",
    "x-att-deviceid": "X-ATT-DeviceId",
    "x-correlation-id": "X-Correlation-ID",
    "x-request-id": "X-Request-ID",
    "x-ua-compatible": "X-UA-Compatible",
    "x-uidh": "X-UIDH",
    "x-webkit-csp": "X-WebKit-CSP",
    "x-xss-protection": "X-XSS-Protection",
}


def meta_to_header(header):
    """
    Normalize an HTTP header as it appears in META.

    >>> meta_to_header("FOO_BAR")
    'Foo-Bar'
    >>> meta_to_header("_")
    '-'

    :param header: Header name
    :return: Normalized header name
    """
    return "-".join(part.capitalize() for part in header.split("_"))


def collect_request_headers(request):
    """
    Given an HTTP request, return its headers as a dictionary.

    :param request: Request object
    :return: Dictionary of headers
    """
    # django 2.2 provides headers already formatted
    if django.VERSION >= (2, 2):
        headers = dict(request.headers.items())
    else:
        # older versions require you to jump through hoops... collect the
        # META keys that start with HTTP_, strip HTTP_ and normalize the
        # remainder to the common header format.
        headers = {
            (meta_to_header(header[5:])): value
            for header, value in request.META.items()
            if header.startswith("HTTP_")
        }
        # Content-Type and Content-Length don't appear as HTTP_
        if "CONTENT_TYPE" in request.META:
            headers["Content-Type"] = request.META["CONTENT_TYPE"]
        if "CONTENT_LENGTH" in request.META:
            headers["Content-Length"] = request.META["CONTENT_LENGTH"]

    out_headers = OrderedDict(headers)
    # replace e.g. Www-Authenticate with WWW-Authenticate, etc.
    for header, value in headers.items():
        known_header = KNOWN_HEADERS.get(header.lower())
        if known_header:
            # replace the header with the new header.  we do it this way to
            # keep the order of the headers intact.
            out_headers = OrderedDict(
                (known_header, v) if header == k else (k, v)
                for (k, v) in out_headers.items()
            )

    # sometimes Content-Length will be the empty string even though it was
    # not sent by the client, so remove it.
    if out_headers.get("Content-Length") == "":
        del out_headers["Content-Length"]

    return out_headers


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


PRETTY_PRINTERS = OrderedDict(
    ((r"/json", pretty_print_json), (r"/xml", pretty_print_xml))
)


def pretty_print(content, content_type):
    for regex, handler in PRETTY_PRINTERS.items():
        if re.search(regex, content_type):
            return handler(content)
    return content
