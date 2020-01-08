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


SPECIAL_HEADERS = {
    header.lower(): header
    for header in [
        "A-IM",
        "ALPN",
        "AMP-Cache-Transform",
        "ARC-Authentication-Results",
        "ARC-Message-Signature",
        "ARC-Seal",
        "C-PEP-Info",
        "C-PEP",
        "Cal-Managed-ID",
        "CalDAV-Timezones",
        "CDN-Loop",
        "Content-ID",
        "Content-MD5",
        "DASL",
        "DAV",
        "Differential-ID",
        "Discarded-X400-IPMS-Extensions",
        "Discarded-X400-MTS-Extensions",
        "DKIM-Signature",
        "DL-Expansion-History",
        "DNT",
        "EDIINT-Features",
        "ETag",
        "Expect-CT",
        "HTTP2-Settings",
        "IM",
        "Include-Referred-Token-Binding-ID",
        "Jabber-ID",
        "List-ID",
        "Message-ID",
        "Message-ID",
        "MIME-Version",
        "MMHS-Acp127-Message-Identifier",
        "MMHS-Authorizing-Users",
        "MMHS-Codress-Message-Indicator",
        "MMHS-Copy-Precedence",
        "MMHS-Exempted-Address",
        "MMHS-Extended-Authorisation-Info",
        "MMHS-Handling-Instructions",
        "MMHS-Message-Instructions",
        "MMHS-Message-Type",
        "MMHS-Originator-PLAD",
        "MMHS-Originator-Reference",
        "MMHS-Other-Recipients-Indicator-CC",
        "MMHS-Other-Recipients-Indicator-To",
        "MMHS-Primary-Precedence",
        "MMHS-Subject-Indicator-Codes",
        "MT-Priority",
        "NNTP-Posting-Date",
        "NNTP-Posting-Host",
        "Optional-WWW-Authenticate",
        "Original-Message-ID",
        "OSCORE",
        "P3P",
        "PEP",
        "PICS-Label",
        "Received-SPF",
        "Resent-Message-ID",
        "SIO-Label-History",
        "SIO-Label",
        "SLUG",
        "Status-URI",
        "SubOK",
        "TCN",
        "TE",
        "TLS-Report-Domain",
        "TLS-Report-Submitter",
        "TLS-Required",
        "TTL",
        "UA-Color",
        "UA-Media",
        "UA-Pixels",
        "UA-Resolution",
        "UA-Windowpixels",
        "URI",
        "VBR-Info",
        "WWW-Authenticate",
        "X-ATT-DeviceId",
        "X-Correlation-ID",
        "X-PGP-Sig",
        "X-Request-ID" "X-Riferimento-Message-ID",
        "X-UA-Compatible",
        "X-UIDH",
        "X-WebKit-CSP",
        "X-XSS-Protection",
        "X400-MTS-Identifier",
    ]
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

    out_headers = OrderedDict()
    # replace e.g. Www-Authenticate with WWW-Authenticate, etc.
    for header, value in headers.items():
        header = SPECIAL_HEADERS.get(header.lower(), header)
        out_headers[header] = value

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
