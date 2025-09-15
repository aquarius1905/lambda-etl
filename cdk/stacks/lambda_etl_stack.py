from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_lambda_event_sources as lambda_event_sources,
    aws_iam as iam,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
import os


class LambdaEtlStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3バケットの作成
        etl_bucket = s3.Bucket(
            self,
            "EtlBucket",
            bucket_name=f"lambda-etl-bucket-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.DESTROY,  # 開発環境用（本番では要注意）
            auto_delete_objects=True,  # 開発環境用（本番では要注意）
            versioned=False,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # SQSキューの作成
        etl_queue = sqs.Queue(
            self,
            "EtlQueue",
            queue_name="lambda-etl-queue",
            visibility_timeout=Duration.minutes(5),  # Lambdaのタイムアウトより長く設定
            retention_period=Duration.days(14),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=3,
                queue=sqs.Queue(
                    self,
                    "EtlDlq",
                    queue_name="lambda-etl-dlq",
                )
            )
        )

        # Lambda関数の作成
        etl_function = _lambda.Function(
            self,
            "EtlFunction",
            function_name="lambda-etl-processor",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="main.lambda_handler",
            code=_lambda.Code.from_asset(
                path="../app",
                exclude=["tests", "__pycache__", "*.pyc"]
            ),
            timeout=Duration.minutes(3),
            memory_size=256,
            environment={
                "S3_BUCKET_NAME": etl_bucket.bucket_name,
                "KEY_PREFIX": "etl-output",
                "PYTHONPATH": "/var/runtime:/var/task",
            },
            retry_attempts=0,  # SQSで再試行を管理
        )

        # Lambda関数にS3への書き込み権限を付与
        etl_bucket.grant_write(etl_function)

        # Lambda関数にSQSからのメッセージ読み取り権限を付与
        etl_queue.grant_consume_messages(etl_function)

        # SQSをLambdaのイベントソースとして設定
        etl_function.add_event_source(
            lambda_event_sources.SqsEventSource(
                etl_queue,
                batch_size=1,  # 一度に1メッセージずつ処理
                max_batching_window=Duration.seconds(5),
                report_batch_item_failures=True,
            )
        )

        # 出力：他のスタックや手動テストで使用するため
        CfnOutput(
            self,
            "BucketName",
            value=etl_bucket.bucket_name,
            description="S3バケット名"
        )

        CfnOutput(
            self,
            "QueueUrl",
            value=etl_queue.queue_url,
            description="SQSキューURL"
        )

        CfnOutput(
            self,
            "QueueName",
            value=etl_queue.queue_name,
            description="SQSキュー名"
        )

        CfnOutput(
            self,
            "FunctionName",
            value=etl_function.function_name,
            description="Lambda関数名"
        )