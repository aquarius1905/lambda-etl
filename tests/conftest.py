import pytest
from unittest.mock import patch
from app.core.config import Settings


@pytest.fixture(autouse=True)
def setup_test_env():
    """テスト用の設定をモック化"""
    test_settings = Settings(
        s3_bucket_name="test-bucket",
        key_prefix="test-output",
        aws_endpoint_url="http://localstack:4566",
    )

    with patch("app.core.config.settings", test_settings):
        yield
