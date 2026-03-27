import pytest


@pytest.fixture
def log_group_event():
    return {"detail": {"requestParameters": {"logGroupName": "/aws/lambda/foo"}}}
