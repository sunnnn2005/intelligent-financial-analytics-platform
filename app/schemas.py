from datetime import date

from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    plaid_transaction_id: str
    merchant_name: str
    category: str
    amount: float
    transaction_date: date


class TransactionOut(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategorySummary(BaseModel):
    category: str
    total_spend: float
    transaction_count: int


class MerchantSummary(BaseModel):
    merchant_name: str
    total_spend: float
    transaction_count: int


class MonthlySummary(BaseModel):
    month: str
    total_spend: float
    transaction_count: int


class DashboardSummary(BaseModel):
    total_spend: float
    transaction_count: int
    top_category: str | None
    top_merchant: str | None
    anomaly_count: int


class AnomalyOut(BaseModel):
    id: int
    merchant_name: str
    category: str
    amount: float
    transaction_date: date
    reason: str
