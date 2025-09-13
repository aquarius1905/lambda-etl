import json
import logging
from app.core.config import settings
from app.core.schema import SQSMessageBody
from app.core.csv_writer import generate_csv
from app.core.s3_uploader import upload_to_s3
from pydantic import ValidationError
from typing import Dict, Any


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info(f"処理開始: {len(event.get('Records', []))}件のメッセージを受信")

    try:
        # SQSのメッセージを取り出す
        if "Records" not in event or len(event["Records"]) == 0:
            raise ValueError("SQSレコードが見つかりません")

        message_body = event["Records"][0]["body"]
        parsed_json = json.loads(message_body)

        # スキーマバリデーション
        payload = SQSMessageBody(**parsed_json)
        records = [record.model_dump() for record in payload.records]

        if not records:
            raise ValueError("処理対象のレコードが存在しません")

        # CSV変換
        csv_data = generate_csv(records)

        # S3にアップロード
        object_key = upload_to_s3(
            settings.s3_bucket_name, settings.key_prefix, csv_data
        )

        logger.info(f"CSV生成完了: {len(records)}件のレコードを処理")
        logger.info(f"S3アップロード完了: {object_key}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "ファイルをアップロードしました",
                    "s3_key": object_key,
                    "processed_records": len(records),
                }
            ),
        }

    except json.JSONDecodeError as e:
        error_msg = f"JSON解析エラー: {str(e)}"
        logger.error(error_msg)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": error_msg}),
        }
    except ValidationError as e:
        error_msg = f"バリデーションエラー: {str(e)}"
        logger.error(error_msg)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": error_msg}),
        }
    except ValueError as e:
        error_msg = f"データエラー発生: {str(e)}"
        logger.error(error_msg)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": error_msg}),
        }
    except Exception as e:
        error_msg = f"予期しないエラー: {str(e)}"
        logger.error(error_msg)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": error_msg}),
        }
