from ddrr.helpers import collect_request_headers
from tests.utils import fake


def test_collect_request_headers(rf):
    """
    collect_request_headers properly formats headers.
    """
    content_type = fake.content_type()
    content_length = fake.random_int()
    request = rf.get(
        "/",
        CONTENT_LENGTH=content_length,
        CONTENT_TYPE=content_type,
        HTTP_FOO_BAR="foo-bar",
        HTTP_HTTP2_SETTINGS="foobar",
    )
    headers = collect_request_headers(request)
    assert dict(headers) == {
        "Content-Length": content_length,  # CONTENT_LENGTH handled
        "Content-Type": content_type,  # CONTENT_TYPE handled
        "Cookie": "",  # added automatically by client
        "Foo-Bar": "foo-bar",  # unknown HTTP_ header
        "HTTP2-Settings": "foobar",  # known HTTP_HEADER
    }


def test_collect_request_headers_drops_empty_content_length(rf):
    """
    collect_request_headers drops empty Content-Length headers.
    """
    request = rf.get("/", CONTENT_LENGTH="")
    headers = collect_request_headers(request)
    assert dict(headers) == {"Cookie": ""}
