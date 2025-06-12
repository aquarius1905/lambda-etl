import json
from app.core.schema import SQSMessageBody
from app.core.csv_writer import generate_csv
from app.core.s3_uploader import upload_to_s3

BUCKET_NAME = "your-bucket-name"
KEY_PREFIX = "etl-output"

def lambda_handler(event, context):
    try:
        # SQSのメッセージを取り出す
        message_body = event["Records"][0]["body"]
        parsed_json = json.loads(message_body)

        # スキーマバリデーション
        payload = SQSMessageBody(**parsed_json)
        records = [record.dict() for record in payload.records]

        # CSV変換
        csv_data = generate_csv(records)

        # S3にアップロード
        object_key = upload_to_s3(BUCKET_NAME, KEY_PREFIX, csv_data)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "ファイルをアップロードしました",
                "s3_key": object_key
            })
        }

    except Exception as e:
        print(f"Error processing the event: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }