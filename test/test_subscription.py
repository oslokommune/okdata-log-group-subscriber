from aws_xray_sdk.core import xray_recorder

from log_group_subscriber.subscription import _log_group_filter_name, _should_subscribe

xray_recorder.begin_segment("Test")


def test_should_subscribe():
    assert _should_subscribe("/aws/lambda/foo")
    assert _should_subscribe("/aws/lambda/foo-bar")
    assert _should_subscribe("/aws/lambda/foo_bar")
    assert not _should_subscribe("/aws/lambda/")
    assert not _should_subscribe("/aws/bambda/foo")
    assert not _should_subscribe("/aws/lambda/foo#")
    assert not _should_subscribe("/aws/lambda/foo-dev-es-logs-plugin")


def test_log_group_filter_name():
    assert _log_group_filter_name("/aws/lambda/foo") == "aws-lambda-foo-filter"
