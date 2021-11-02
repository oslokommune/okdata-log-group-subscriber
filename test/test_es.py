from log_group_subscriber.es import _es_body_from_log_event


def test_es_body_from_log_event(log_event):
    body = _es_body_from_log_event(log_event)

    assert body["service_name"] == "foo"
    assert body["@id"] == "9481760491939405"
    assert body["@message"] == log_event["message"]
    assert body["@timestamp"] == "2021-11-02T14:19:32.240285Z"
