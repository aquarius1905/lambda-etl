# tests/conftest.py
import os
import pytest

# モジュールレベルで環境変数を設定（importより前に実行される）
os.environ.setdefault('AWS_ENDPOINT_URL', 'http://localhost:4566')
os.environ.setdefault('AWS_REGION', 'us-east-1')

@pytest.fixture(autouse=True)
def setup_test_env():
    """テスト実行時に自動で環境変数を設定"""
    # 既に上で設定済みだが、明示的に設定
    os.environ['AWS_ENDPOINT_URL'] = 'http://localhost:4566'
    os.environ['AWS_REGION'] = 'us-east-1'
    yield