from pydantic import BaseModel, Field
from typing import List

class DataRecord(BaseModel):
    user_id: int = Field(..., example=123)
    name: str = Field(..., example="山田太郎")
    email: str = Field(..., example="taro@example.com")

class SQSMessageBody(BaseModel):
    records: List[DataRecord]