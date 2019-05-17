import django
from django.conf import settings

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "ddrr-request-formatter": {
            "()": "ddrr.formatters.DefaultRequestFormatter",
            "pretty": True,
        },
        "ddrr-response-formatter": {
            "()": "ddrr.formatters.DefaultResponseFormatter",
            "pretty": True,
        },
    },
    "handlers": {
        "ddrr-request-handler": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "ddrr-request-formatter",
        },
        "ddrr-response-handler": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "ddrr-response-formatter",
        },
    },
    "loggers": {
        "ddrr-request-logger": {"handlers": ["ddrr-request-handler"], "level": "DEBUG"},
        "ddrr-response-logger": {
            "handlers": ["ddrr-response-handler"],
            "level": "DEBUG",
        },
    },
}

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
        # older versions require you to jump through hoops... collect the META keys that
        # start with HTTP_, strip HTTP_ and normalize the remainder to the common header
        # format.
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
    # sometimes Content-Length will be the empty string even though it was not sent by
    # the client, so remove it.
    if headers.get("Content-Length", "1") == "":
        del headers["Content-Length"]
    return headers


def collect_response_headers(response):
    """
    Given an HTTP response, return its headers as a dictionary.
    :param response: Response object
    :return: Dictionary of headers
    """
    return dict(response.items())


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


def quick_setup():
    # set up logging
    merge(DEFAULT_LOGGING_CONFIG, settings.LOGGING)
    # set up middleware
    if "ddrr.middleware.DebugRequestsResponses" not in settings.MIDDLEWARE:
        settings.MIDDLEWARE.insert(0, "ddrr.middleware.DebugRequestsResponses")


def configure_requests(level=None, pretty=None, template=None, template_name=None):
    formatter = {}
    logger = {}
    if level:
        logger["level"] = level
    if template:
        formatter["template"] = template
    if template_name:
        formatter["template_name"] = template_name
    if pretty is not None:
        formatter["pretty"] = pretty
    merge(
        {"ddrr-request-formatter": formatter, "ddrr-request-logger": logger},
        settings.LOGGING,
    )
