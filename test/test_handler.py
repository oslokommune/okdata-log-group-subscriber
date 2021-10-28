from unittest.mock import Mock, patch

from aws_xray_sdk.core import xray_recorder

from log_group_subscriber.handler import (
    _log_group_filter_name,
    _should_subscribe,
    handle_new_log_group,
)

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


def test_handle_new_log_group():
    with patch("log_group_subscriber.handler.boto3") as mock_boto:
        mock_logs_client = Mock()
        mock_boto.client.return_value = mock_logs_client

        handle_new_log_group(
            {"detail": {"requestParameters": {"logGroupName": "/aws/lambda/foo"}}},
            None,
        )

        mock_logs_client.put_subscription_filter.assert_called_once()
