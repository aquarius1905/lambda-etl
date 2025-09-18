from typing import List

from pydantic import BaseModel, Field


class DataRecord(BaseModel):
    user_id: int = Field(..., description="ユーザーID")
    name: str = Field(..., description="ユーザー名")
    email: str = Field(..., description="メールアドレス")


class SQSMessageBody(BaseModel):
    records: List[DataRecord]
