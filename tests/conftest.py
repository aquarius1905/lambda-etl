from unittest.mock import patch

import pytest

from app.core.config import Settings


@pytest.fixture(autouse=True)
def setup_test_env():
    """テスト用の設定をモック化"""
    test_settings = Settings(
        S3_BUCKET_NAME="test-bucket",
        KEY_PREFIX="test-output",
    )

    with patch("app.core.config.settings", test_settings):
        yield
