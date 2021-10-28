import os
import re

import boto3
from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper

from log_group_subscriber.util import getenv

patch_all()

DESTINATION_ARN = getenv("DESTINATION_ARN")
SUBSCRIPTION_WHITELIST = os.getenv("SUBSCRIPTION_WHITELIST", None)
SUBSCRIPTION_BLACKLIST = os.getenv("SUBSCRIPTION_BLACKLIST", None)
FILTER_PATTERN = getenv("FILTER_PATTERN")


def _should_subscribe(log_group_name):
    """Return True if a subscription should be made for `log_group_name`."""
    if SUBSCRIPTION_WHITELIST:
        if not re.compile(SUBSCRIPTION_WHITELIST).fullmatch(log_group_name):
            return False

    if SUBSCRIPTION_BLACKLIST:
        if re.compile(SUBSCRIPTION_BLACKLIST).search(log_group_name):
            return False

    return True


def _log_group_filter_name(log_group_name):
    """Return the filter name to use for the log group named `log_group_name`."""
    return "{}-filter".format(log_group_name.strip("/").replace("/", "-"))


def _handle_new_log_group(log_group_name):
    """Handle a new log group.

    Return True if a subscription was created, otherwise return False.
    """
    if not _should_subscribe(log_group_name):
        return False

    boto3.client("logs").put_subscription_filter(
        destinationArn=DESTINATION_ARN,
        filterName=_log_group_filter_name(log_group_name),
        filterPattern=FILTER_PATTERN,
        logGroupName=log_group_name,
    )

    return True


@logging_wrapper
@xray_recorder.capture("handle_new_log_group")
def handle_new_log_group(event, context):
    _handle_new_log_group(event["detail"]["requestParameters"]["logGroupName"])
