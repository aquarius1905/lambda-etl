import pytest
from unittest.mock import patch
from app.core.config import Settings


@pytest.fixture(autouse=True)
def setup_test_env():
    """テスト用の設定をモック化"""
    test_settings = Settings(
        S3_BUCKET_NAME="test-bucket",
        KEY_PREFIX="test-output",
        AWS_ENDPOINT_URL="http://localstack:4566",
    )

    with patch("app.core.config.settings", test_settings):
        yield
