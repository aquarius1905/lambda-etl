from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_prefix="APP_")

    s3_bucket_name: str = Field(default="your-bucket-name", alias="S3_BUCKET_NAME")
    key_prefix: str = Field(default="etl-output", alias="KEY_PREFIX")


settings = Settings()
