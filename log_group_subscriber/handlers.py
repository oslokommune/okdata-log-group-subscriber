from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper

from log_group_subscriber.subscription import handle_new_log_group

patch_all()


@logging_wrapper
@xray_recorder.capture("new_log_group")
def new_log_group(event, context):
    handle_new_log_group(event["detail"]["requestParameters"]["logGroupName"])
