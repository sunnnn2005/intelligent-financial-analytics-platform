from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.analytics import detect_anomalies, summarize_by_category
from app.database import Base, engine, get_db
from app.models import Transaction
from app.schemas import AnomalyOut, CategorySummary, TransactionCreate, TransactionOut
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


@app.get("/analytics/category-summary", response_model=list[CategorySummary])
def category_summary(db: Session = Depends(get_db)):
    rows = [
        {
            "category": transaction.category,
            "amount": transaction.amount,
        }
        for transaction in db.query(Transaction).all()
    ]
    return summarize_by_category(rows)


@app.get("/analytics/anomalies", response_model=list[AnomalyOut])
def anomalies(db: Session = Depends(get_db)):
    rows = [
        {
            "id": transaction.id,
            "merchant_name": transaction.merchant_name,
            "category": transaction.category,
            "amount": transaction.amount,
            "transaction_date": transaction.transaction_date,
        }
        for transaction in db.query(Transaction).all()
    ]
    return detect_anomalies(rows)
