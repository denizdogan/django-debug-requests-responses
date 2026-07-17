from ddrr.records import RequestLogRecord
from ddrr.records import ResponseLogRecord


def test_request_log_record_accepts_formatter_alias():
    record = object()
    request = object()
    formatter = object()

    log_record = RequestLogRecord(
        record=record,
        request=request,
        formatter=formatter,
    )

    assert log_record.record is record
    assert log_record.request is request
    assert log_record._formatter is formatter
    assert vars(log_record) == {
        "record": record,
        "request": request,
        "_formatter": formatter,
    }


def test_response_log_record_accepts_formatter_alias():
    record = object()
    response = object()
    formatter = object()

    log_record = ResponseLogRecord(
        record=record,
        response=response,
        formatter=formatter,
    )

    assert log_record.record is record
    assert log_record.response is response
    assert log_record._formatter is formatter
    assert vars(log_record) == {
        "record": record,
        "response": response,
        "_formatter": formatter,
    }
