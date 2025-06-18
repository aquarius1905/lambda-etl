import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    s3_bucket_name: str = "your-bucket-name"
    key_prefix: str = "etl-output"
    aws_endpoint_url: str = None
    
    class Config:
        env_prefix = ""

settings = Settings()