from datetime import datetime

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float = Field(gt=0)
    currency: str
    timestamp: datetime
    merchant: str | None = None
