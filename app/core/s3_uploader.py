import boto3
import os
from datetime import datetime, UTC

def get_s3_client():
    endpoint_url = os.environ.get("AWS_ENDPOINT_URL")
    if endpoint_url:
        return boto3.client("s3", endpoint_url=endpoint_url)
    return boto3.client("s3")

def upload_to_s3(bucket_name: str, key_prefix: str, csv_content: str) -> str:
    s3 = get_s3_client()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{key_prefix}/output_{timestamp}.csv"

    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=csv_content.encode("utf-8"),
        ContentType="text/csv"
    )

    return object_key