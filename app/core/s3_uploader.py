
import boto3
from datetime import datetime

s3 = boto3.client("s3")

def upload_to_s3(bucket_name: str, key_prefix: str, csv_content: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    object_key = f"{key_prefix}/output_{timestamp}.csv"

    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=csv_content.encode("utf-8"),
        ContentType="text/csv"
    )

    return object_key