from datetime import date

MOCK_TRANSACTIONS = [
    {
        "plaid_transaction_id": "txn_001",
        "merchant_name": "Trader Joe's",
        "category": "Groceries",
        "amount": 54.23,
        "transaction_date": date(2026, 7, 1),
    },
    {
        "plaid_transaction_id": "txn_002",
        "merchant_name": "Target",
        "category": "Shopping",
        "amount": 87.12,
        "transaction_date": date(2026, 7, 2),
    },
    {
        "plaid_transaction_id": "txn_003",
        "merchant_name": "Philz Coffee",
        "category": "Dining",
        "amount": 6.75,
        "transaction_date": date(2026, 7, 3),
    },
    {
        "plaid_transaction_id": "txn_004",
        "merchant_name": "Chevron",
        "category": "Transportation",
        "amount": 63.98,
        "transaction_date": date(2026, 7, 5),
    },
    {
        "plaid_transaction_id": "txn_005",
        "merchant_name": "Apple Store",
        "category": "Electronics",
        "amount": 1299.0,
        "transaction_date": date(2026, 7, 8),
    },
    {
        "plaid_transaction_id": "txn_006",
        "merchant_name": "Safeway",
        "category": "Groceries",
        "amount": 42.11,
        "transaction_date": date(2026, 7, 9),
    },
]
