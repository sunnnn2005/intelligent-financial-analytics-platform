from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.database import Base, get_db
from app.main import app


def build_client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        pool_pre_ping=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_seed_and_dashboard_summary():
    client = build_client()

    seed_response = client.post("/seed")
    assert seed_response.status_code == 200
    assert len(seed_response.json()) >= 1

    summary_response = client.get("/analytics/dashboard")
    assert summary_response.status_code == 200
    summary = summary_response.json()

    assert summary["transaction_count"] >= 1
    assert summary["total_spend"] > 0
    assert summary["top_category"] is not None


def test_duplicate_transaction_returns_conflict():
    client = build_client()
    payload = {
        "plaid_transaction_id": "txn_test_001",
        "merchant_name": "Test Merchant",
        "category": "Testing",
        "amount": 12.34,
        "transaction_date": "2026-07-13",
    }

    assert client.post("/transactions", json=payload).status_code == 200
    duplicate_response = client.post("/transactions", json=payload)

    assert duplicate_response.status_code == 409


def test_dashboard_page_renders():
    client = build_client()
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Financial Analytics Dashboard" in response.text
