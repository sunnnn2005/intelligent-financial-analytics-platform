from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.analytics import (
    build_dashboard_summary,
    detect_anomalies,
    summarize_by_category,
    summarize_by_merchant,
    summarize_by_month,
)
from app.database import Base, engine, get_db
from app.dashboard import render_dashboard
from app.models import Transaction
from app.schemas import (
    AnomalyOut,
    CategorySummary,
    DashboardSummary,
    MerchantSummary,
    MonthlySummary,
    TransactionCreate,
    TransactionOut,
)
from app.seed_data import MOCK_TRANSACTIONS

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Financial Analytics Platform")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions", response_model=TransactionOut)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(**payload.model_dump())
    db.add(transaction)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Transaction already exists") from exc

    db.refresh(transaction)
    return transaction


@app.post("/seed", response_model=list[TransactionOut])
def seed_transactions(db: Session = Depends(get_db)):
    created = []
    for item in MOCK_TRANSACTIONS:
        exists = (
            db.query(Transaction)
            .filter(Transaction.plaid_transaction_id == item["plaid_transaction_id"])
            .first()
        )
        if exists:
            continue

        transaction = Transaction(**item)
        db.add(transaction)
        created.append(transaction)

    db.commit()
    for transaction in created:
        db.refresh(transaction)
    return created


@app.get("/transactions", response_model=list[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.transaction_date.desc()).all()


def transaction_rows(db: Session):
    return [
        {
            "id": transaction.id,
            "merchant_name": transaction.merchant_name,
            "category": transaction.category,
            "amount": transaction.amount,
            "transaction_date": transaction.transaction_date,
        }
        for transaction in db.query(Transaction).all()
    ]


@app.get("/analytics/category-summary", response_model=list[CategorySummary])
def category_summary(db: Session = Depends(get_db)):
    return summarize_by_category(transaction_rows(db))


@app.get("/analytics/merchant-summary", response_model=list[MerchantSummary])
def merchant_summary(db: Session = Depends(get_db)):
    return summarize_by_merchant(transaction_rows(db))


@app.get("/analytics/monthly-summary", response_model=list[MonthlySummary])
def monthly_summary(db: Session = Depends(get_db)):
    return summarize_by_month(transaction_rows(db))


@app.get("/analytics/dashboard", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    return build_dashboard_summary(transaction_rows(db))


@app.get("/analytics/anomalies", response_model=list[AnomalyOut])
def anomalies(db: Session = Depends(get_db)):
    return detect_anomalies(transaction_rows(db))


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return render_dashboard()
