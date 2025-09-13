from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_prefix="")

    s3_bucket_name: str = Field(default="your-bucket-name", alias="S3_BUCKET_NAME")
    key_prefix: str = Field(default="etl-output", alias="KEY_PREFIX")
    aws_endpoint_url: Optional[str] = Field(default=None, alias="AWS_ENDPOINT_URL")


settings = Settings()
