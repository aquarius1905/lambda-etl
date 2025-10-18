#!/bin/bash

# Lambda関数デプロイパッケージ作成スクリプト

set -e

echo "=== Lambda デプロイパッケージ作成開始 ==="

# プロジェクトルートディレクトリで実行されているか確認
if [ ! -d "app" ]; then
    echo "エラー: appディレクトリが見つかりません"
    echo "プロジェクトルートで実行してください"
    exit 1
fi

# 既存のデプロイパッケージを削除
echo "既存のデプロイパッケージをクリーンアップ..."
rm -rf deploy-package
rm -f lambda-etl-function.zip

# デプロイ用ディレクトリを作成
echo "デプロイ用ディレクトリを作成..."
mkdir deploy-package

# 依存ライブラリをインストール
echo "依存ライブラリをインストール..."
pip install boto3 pydantic pydantic-settings -t deploy-package/
s
# appディレクトリをコピー（不要なファイルを除外）
echo "アプリケーションコードをコピー..."
rsync -av \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='.pytest_cache' \
  --exclude='.coverage' \
  --exclude='htmlcov' \
  --exclude='*.log' \
  --exclude='.DS_Store' \
  app deploy-package/

# zipファイルを作成
echo "zipファイルを作成..."
cd deploy-package
zip -r ../lambda-etl-function.zip . -x "*.pyc" -x "*__pycache__*"
cd ..

# パッケージサイズを表示
PACKAGE_SIZE=$(du -h lambda-etl-function.zip | cut -f1)
echo ""
echo "=== デプロイパッケージ作成完了 ==="
echo "ファイル: lambda-etl-function.zip"
echo "サイズ: $PACKAGE_SIZE"
echo ""
echo "次のステップ:"
echo "1. AWS Lambda コンソールでlambda-etl-function.zipをアップロード"
echo "2. ハンドラーが 'app.main.lambda_handler' になっていることを確認"
echo ""

# パッケージ内容を確認（オプション）
read -p "パッケージ内容を確認しますか? (y/N): " confirm
if [[ $confirm == [yY] ]]; then
    echo ""
    echo "=== パッケージ内容 ==="
    unzip -l lambda-etl-function.zip
fi