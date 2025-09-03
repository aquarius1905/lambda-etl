from app.core.csv_writer import generate_csv
from app.core.schema import DataRecord, SQSMessageBody
import pytest


class TestCSVWriter:
    def test_generate_csv_success(self):
        """CSV生成の正常系テスト"""
        records = [
            {"user_id": 1, "name": "山田太郎", "email": "taro@example.com"},
            {"user_id": 2, "name": "佐藤花子", "email": "hanako@example.com"},
        ]

        result = generate_csv(records)

        assert "user_id,name,email" in result
        assert "山田太郎" in result
        assert "佐藤花子" in result

    def test_generate_csv_empty_records(self):
        """空のレコードでのCSV生成テスト"""
        with pytest.raises(ValueError, match="CSV出力対象のデータが空です"):
            generate_csv([])


class TestSchema:
    def test_data_record_validation_success(self):
        """DataRecordの正常なバリデーション"""
        record = DataRecord(
            user_id=123, name="テストユーザー", email="test@example.com"
        )

        assert record.user_id == 123
        assert record.name == "テストユーザー"
        assert record.email == "test@example.com"

    def test_sqs_message_body_validation_success(self):
        """SQSMessageBodyの正常なバリデーション"""
        data = {
            "records": [{"user_id": 1, "name": "山田太郎", "email": "taro@example.com"}]
        }

        message = SQSMessageBody(**data)

        assert len(message.records) == 1
        assert message.records[0].user_id == 1
