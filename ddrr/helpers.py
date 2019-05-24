import django


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
    # replace e.g. Www-Authenticate with WWW-Authenticate, etc.
    for header, value in headers.items():
        known_header = KNOWN_HEADERS.get(header.lower())
        if known_header:
            del headers[header]
            headers[known_header] = value
    # sometimes Content-Length will be the empty string even though it was
    # not sent by the client, so remove it.
    if headers.get("Content-Length", "1") == "":
        del headers["Content-Length"]
    return headers


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


def merge(source, destination):
    """
    Destructively and recursively merge two dictionaries. Return the result.
    Copied from https://stackoverflow.com/a/20666342.

    >>> merge({'a': 1, 'b': 2}, {'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    True
    >>> merge({'a': {'b': 1}}, {'c': 2}) == {'a': {'b': 1}, 'c': 2}
    True
    >>> merge({'a': {'b': 1}}, {}) == {'a': {'b': 1}}
    True
    >>> merge({'a': {'b': 1}}, {'a': {'b': 2}}) == {'a': {'b': 1}}
    True
    >>> merge({'a': 1}, {'a': {'b': 2}}) == {'a': 1}
    True

    :param source: Source dictionary
    :param destination: Destination dictionary
    :returns: The destination dictionary
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value
    return destination
