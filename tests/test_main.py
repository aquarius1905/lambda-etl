from unittest.mock import patch, MagicMock
import json
from app.main import lambda_handler

@patch('app.main.boto3.client')
def test_lambda_handler_success(mock_boto3_client):
    # S3クライアントのモック
    mock_s3 = MagicMock()
    mock_boto3_client.return_value = mock_s3
    
    event = {
        "Records": [
            {
                "body": json.dumps({
                    "records": [
                        {"user_id": 1, "name": "山田太郎", "email": "taro@example.com"},
                        {"user_id": 2, "name": "佐藤花子", "email": "hanako@example.com"}
                    ]
                })
            }
        ]
    }
    
    response = lambda_handler(event, None)
    
    # 自分のコードが正しくS3クライアントを呼び出したかを検証
    mock_boto3_client.assert_called_with('s3')
    mock_s3.put_object.assert_called_once()
    
    # レスポンスの検証（自分のコードのロジック）
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "s3_key" in body