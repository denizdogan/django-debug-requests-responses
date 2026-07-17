from types import SimpleNamespace

from django.http import HttpResponse

from ddrr.filters import StatusCodeFilter


def test_response_status_code_filters_disallowed():
    """
    StatusCodeFilter filters out responses with disallowed status codes.
    """
    status_code_filter = StatusCodeFilter(status_codes="401")
    response = HttpResponse("foo", status=401)
    record = SimpleNamespace(msg=response)
    assert not status_code_filter.filter(record)


def test_response_status_code_does_not_filter_allowed():
    """
    StatusCodeFilter does not filter out responses with allowed status codes.
    """
    status_code_filter = StatusCodeFilter(status_codes="401")
    response = HttpResponse("foo", status=404)
    record = SimpleNamespace(msg=response)
    assert status_code_filter.filter(record)


def test_response_status_code_does_not_filter_unknown():
    """
    StatusCodeFilter does not filter out responses which have no status code
    attribute.
    """
    status_code_filter = StatusCodeFilter(status_codes="401")
    response = object()
    record = SimpleNamespace(msg=response)
    assert status_code_filter.filter(record)
