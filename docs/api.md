# API Reference

Base URL for local development:

```text
http://localhost:8000
```

## Core Endpoints

### `GET /health`

Returns service health.

### `POST /transactions`

Creates a transaction record.

Example body:

```json
{
  "date": "2026-07-15",
  "merchant": "Trader Joe's",
  "category": "Groceries",
  "amount": 28.42
}
```

### `POST /plaid/sync/mock`

Loads mock Plaid Sandbox-style transactions.

### `POST /seed`

Seeds the local database with demo transactions for dashboards and API testing.

## Analytics Endpoints

### `GET /analytics/category-summary`

Returns spending grouped by category.

### `GET /analytics/merchant-summary`

Returns spending grouped by merchant.

### `GET /analytics/monthly-summary`

Returns spending grouped by month.

### `GET /analytics/anomalies`

Returns transactions flagged as unusually large.

### `GET /analytics/dashboard`

Returns dashboard-ready metrics such as total spend, transaction count, top
category, top merchant, and anomaly count.
