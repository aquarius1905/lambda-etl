import aws_cdk as cdk
from stacks.lambda_etl_stack import LambdaEtlStack

app = cdk.App()

# 環境の設定
env = cdk.Environment(
    account=app.node.try_get_context("account"),
    region=app.node.try_get_context("region") or "ap-northeast-1"
)

# スタックの作成
LambdaEtlStack(
    app, 
    "LambdaEtlStack",
    env=env,
    description="ETL処理用のLambda、SQS、S3リソース"
)

app.synth()