from datetime import date

from freezegun import freeze_time

from log_group_subscriber.es import _es_body_from_log_event, _index_name, _log_date


def test_es_body_from_log_event(log_event):
    body = _es_body_from_log_event(log_event)

    assert body["service_name"] == "foo"
    assert body["@id"] == "9481760491939405"
    assert body["@message"] == log_event["message"]
    assert body["@timestamp"] == "2021-11-02T14:19:32.240285Z"


def test_log_date(log_event):
    assert _log_date(_es_body_from_log_event(log_event)) == date(2021, 11, 2)


@freeze_time("2020-01-01T16:00:00+00:00")
def test_log_date_missing_timestamp(log_event):
    body = _es_body_from_log_event(log_event)
    del body["timestamp"]
    assert _log_date(body) == date(2020, 1, 1)


def test_index_name(log_event):
    body = _es_body_from_log_event(log_event)
    assert _index_name(body) == "dataplatform-services-2021-11-02"


@freeze_time("2020-01-01T16:00:00+00:00")
def test_index_name_missing_timestamp(log_event):
    body = _es_body_from_log_event(log_event)
    del body["timestamp"]
    assert _index_name(body) == "dataplatform-services-2020-01-01"
