import gzip
import json
from base64 import b64decode
from datetime import datetime
from zoneinfo import ZoneInfo

import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from log_group_subscriber.util import getenv

AWS_REGION = getenv("AWS_REGION")
ES_API_ENDPOINT = getenv("ES_API_ENDPOINT")
ES_INDEX_PREFIX = getenv("ES_INDEX_PREFIX")

_ES_CLIENT = None


def _es_client():
    global _ES_CLIENT

    if not _ES_CLIENT:
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            AWS_REGION,
            "es",
            session_token=credentials.token,
        )
        _ES_CLIENT = Elasticsearch(
            hosts=[{"host": ES_API_ENDPOINT, "scheme": "https", "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=2,
        )
    return _ES_CLIENT


def _es_body_from_log_event(log_event):
    body = json.loads(log_event["message"])

    if "id" in log_event:
        body["@id"] = log_event["id"]
    if "timestamp" in body:
        body["@timestamp"] = body["timestamp"]
    if "message" in log_event:
        body["@message"] = log_event["message"]

    return body


def cloudwatch_to_es(event):
    es = _es_client()
    index = "{}-{}".format(
        ES_INDEX_PREFIX,
        datetime.now(ZoneInfo("Europe/Oslo")).date().isoformat(),
    )
    message = json.loads(
        gzip.decompress(b64decode(event["awslogs"]["data"])).decode("utf-8")
    )
    for body in map(_es_body_from_log_event, message["logEvents"]):
        es.index(index=index, doc_type="log", body=body)
