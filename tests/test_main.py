import json
from unittest.mock import MagicMock, patch

from app.main import lambda_handler


class TestLambdaHandler:

    @patch("app.core.s3_uploader.boto3.client")
    def test_lambda_handler_success(self, mock_boto3_client):
        # S3クライアントのモック
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "records": [
                                {
                                    "user_id": 1,
                                    "name": "山田太郎",
                                    "email": "taro@example.com",
                                },
                                {
                                    "user_id": 2,
                                    "name": "佐藤花子",
                                    "email": "hanako@example.com",
                                },
                            ]
                        }
                    )
                }
            ]
        }

        response = lambda_handler(event, None)

        # 自分のコードが正しくS3クライアントを呼び出したかを検証
        # 環境変数AWS_ENDPOINT_URLが設定されているため、endpoint_urlパラメータ付きで呼ばれる
        mock_boto3_client.assert_called_with(
            "s3", endpoint_url="http://localstack:4566"
        )
        mock_s3.put_object.assert_called_once()

        # put_objectの引数をより詳しく検証
        call_args = mock_s3.put_object.call_args
        assert call_args[1]["Bucket"] == "lambda-etl-bucket"
        assert call_args[1]["Key"].startswith("etl-output/output_")
        assert call_args[1]["Key"].endswith(".csv")
        assert call_args[1]["ContentType"] == "text/csv"

        # レスポンスの検証
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "s3_key" in body
        assert "processed_records" in body
        assert body["processed_records"] == 2

    def test_lambda_handler_no_records(self):
        """SQSレコードがない場合のテスト"""
        event = {"Records": []}

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "SQSレコードが見つかりません" in body["error"]

    def test_lambda_handler_invalid_json(self):
        """無効なJSONの場合のテスト"""
        event = {"Records": [{"body": "invalid json"}]}

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "JSON解析エラー" in body["error"]

    def test_lambda_handler_empty_records(self):
        """空のレコードリストの場合のテスト"""
        event = {"Records": [{"body": json.dumps({"records": []})}]}

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "処理対象のレコードが存在しません" in body["error"]

    def test_lambda_handler_validation_error(self):
        """バリデーションエラーの場合のテスト"""
        event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "records": [
                                {
                                    "user_id": "invalid",
                                    "name": "山田太郎",
                                    "email": "taro@example.com",
                                }
                            ]
                        }
                    )
                }
            ]
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "バリデーションエラー" in body["error"]

    @patch("app.core.s3_uploader.boto3.client")
    def test_lambda_handler_s3_error(self, mock_boto3_client):
        """S3アップロードエラーの場合のテスト"""
        # S3クライアントのモック
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = Exception("S3 upload failed")
        mock_boto3_client.return_value = mock_s3

        event = {
            "Records": [
                {
                    "body": json.dumps(
                        {
                            "records": [
                                {
                                    "user_id": 1,
                                    "name": "山田太郎",
                                    "email": "taro@example.com",
                                }
                            ]
                        }
                    )
                }
            ]
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "予期しないエラー" in body["error"]
