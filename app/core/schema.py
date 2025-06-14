from pydantic import BaseModel, Field
from typing import List

class DataRecord(BaseModel):
    user_id: int = Field(..., description="ユーザーID")
    name: str = Field(..., description="ユーザー名")
    email: str = Field(..., description="メールアドレス")

class SQSMessageBody(BaseModel):
    records: List[DataRecord]