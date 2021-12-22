from unittest.mock import Mock, patch

from aws_xray_sdk.core import xray_recorder

from log_group_subscriber.handlers import cloudwatch_event, new_log_group

xray_recorder.begin_segment("Test")


def test_new_log_group(log_group_event):
    with patch("log_group_subscriber.subscription.boto3") as mock_boto:
        mock_logs_client = Mock()
        mock_boto.client.return_value = mock_logs_client

        new_log_group(log_group_event, None)

        mock_logs_client.put_subscription_filter.assert_called_once()


def test_cloudwatch_event(cw_event):
    with patch("log_group_subscriber.es._es_client") as _es_client:
        mock_es_client = Mock()
        _es_client.return_value = mock_es_client

        cloudwatch_event(cw_event, None)

        mock_es_client.index.assert_called_once()
