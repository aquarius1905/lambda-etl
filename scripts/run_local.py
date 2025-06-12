import json
from app.main import lambda_handler

event = {
    "Records": [
        {
            "body": json.dumps({
                "records": [
                    {"user_id": 1, "name": "山田太郎", "email": "taro@example.com"}
                ]
            })
        }
    ]
}

if __name__ == "__main__":
    response = lambda_handler(event, None)
    print(response)