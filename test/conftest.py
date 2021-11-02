import base64
import gzip
import json

import pytest


@pytest.fixture
def log_group_event():
    return {"detail": {"requestParameters": {"logGroupName": "/aws/lambda/foo"}}}


@pytest.fixture
def log_event():
    return {
        "id": "9481760491939405",
        "timestamp": 1635862772240,
        "message": '{"service_name": "foo", "handler_method": "async_handler", "function_name": "foo-dev-bar", "function_version": "$LATEST", "function_stage": "dev", "function_api_id": "6fc30dd3c8", "git_rev": "test:842694b", "aws_account_id": "123456789101", "aws_request_id": "d0908999-c343-6e1b-36a8-afb246b38387", "aws_trace_id": "Root=0-2df94e61-38c671fee0cb1bc0450068f3", "memory_limit_in_mb": "128", "logged_in": false, "principal_id": null, "source_ip": "123.45.678.x", "request_domain_name": "1ceb9b5668.execute-api.eu-west-1.amazonaws.com", "request_resource": "/", "request_path": "/", "request_method": "GET", "request_path_parameters": null, "request_query_string_parameters": {}, "cold_start": true, "hello": "world", "response_status_code": 200, "level": "info", "duration_ms": 59.042201, "event": "", "timestamp": "2021-11-02T14:19:32.240285Z"}\n',
    }


@pytest.fixture
def cw_event(log_event):
    return {
        "awslogs": {
            "data": base64.b64encode(
                gzip.compress(
                    json.dumps(
                        {
                            "messageType": "DATA_MESSAGE",
                            "owner": "123456789101",
                            "logGroup": "/aws/lambda/foo",
                            "logStream": "2021/11/02/[$LATEST]ecb0714347e39edfa12a7d6173da8fd1",
                            "subscriptionFilters": ["aws-lambda-foo-dev-bar-filter"],
                            "logEvents": [log_event],
                        }
                    ).encode("utf-8")
                )
            )
        }
    }
