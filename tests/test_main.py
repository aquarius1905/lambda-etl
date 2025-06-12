import json
from app.main import lambda_handler

def test_lambda_handler_success():
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
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "s3_key" in body