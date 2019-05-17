from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse


def test_request_and_response_are_logged(client, caplog):
    """
    Requests and responses are logged.
    """
    client.get(reverse("index"))
    assert isinstance(caplog.records[0].msg, HttpRequest)
    assert isinstance(caplog.records[1].msg, HttpResponse)
    assert len(caplog.records) == 2
