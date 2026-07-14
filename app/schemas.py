from datetime import date

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    plaid_transaction_id: str
    merchant_name: str
    category: str
    amount: float
    transaction_date: date


class TransactionOut(TransactionCreate):
    id: int

    class Config:
        from_attributes = True


class CategorySummary(BaseModel):
    category: str
    total_spend: float
    transaction_count: int


class AnomalyOut(BaseModel):
    id: int
    merchant_name: str
    category: str
    amount: float
    transaction_date: date
    reason: str
