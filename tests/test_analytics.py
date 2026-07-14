from datetime import date

from app.analytics import (
    build_dashboard_summary,
    detect_anomalies,
    summarize_by_category,
    summarize_by_merchant,
    summarize_by_month,
)


ROWS = [
    {
        "id": 1,
        "merchant_name": "Trader Joe's",
        "category": "Groceries",
        "amount": 54.23,
        "transaction_date": date(2026, 7, 1),
    },
    {
        "id": 2,
        "merchant_name": "Safeway",
        "category": "Groceries",
        "amount": 42.11,
        "transaction_date": date(2026, 7, 9),
    },
    {
        "id": 3,
        "merchant_name": "Apple Store",
        "category": "Electronics",
        "amount": 1299.00,
        "transaction_date": date(2026, 7, 8),
    },
    {
        "id": 4,
        "merchant_name": "Philz Coffee",
        "category": "Dining",
        "amount": 6.75,
        "transaction_date": date(2026, 8, 3),
    },
]


def test_summarize_by_category_orders_by_spend():
    summary = summarize_by_category(ROWS)

    assert summary[0]["category"] == "Electronics"
    assert summary[1]["category"] == "Groceries"
    assert summary[1]["transaction_count"] == 2


def test_summarize_by_merchant_orders_by_spend():
    summary = summarize_by_merchant(ROWS)

    assert summary[0]["merchant_name"] == "Apple Store"
    assert summary[0]["total_spend"] == 1299.00


def test_summarize_by_month_groups_dates():
    summary = summarize_by_month(ROWS)

    assert summary[0]["month"] == "2026-07"
    assert summary[0]["transaction_count"] == 3
    assert summary[1]["month"] == "2026-08"


def test_detect_anomalies_flags_large_transaction():
    anomalies = detect_anomalies(ROWS)

    assert len(anomalies) == 1
    assert anomalies[0]["merchant_name"] == "Apple Store"
    assert "dynamic threshold" in anomalies[0]["reason"]


def test_dashboard_summary_returns_portfolio_metrics():
    summary = build_dashboard_summary(ROWS)

    assert summary["transaction_count"] == 4
    assert summary["top_category"] == "Electronics"
    assert summary["top_merchant"] == "Apple Store"
    assert summary["anomaly_count"] == 1
