from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = ConfigDict(env_prefix="")
    
    s3_bucket_name: str = "your-bucket-name"
    key_prefix: str = "etl-output"
    aws_endpoint_url: str = None

settings = Settings()