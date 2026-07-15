# Architecture

This project is a backend analytics service for personal finance data. It is
designed to show API design, relational data modeling, transaction cleaning, and
dashboard-ready analytics.

## Components

- **FastAPI app:** Exposes transaction ingestion, mock sync, health, dashboard,
  and analytics endpoints.
- **SQLAlchemy models:** Store transaction records in a relational schema.
- **Analytics layer:** Uses pandas and NumPy to compute category, merchant,
  monthly, and anomaly summaries.
- **Mock Plaid sync:** Generates sandbox-style transactions without requiring
  paid Plaid credentials.
- **Dashboard route:** Renders a lightweight local dashboard for demo purposes.

## Data Flow

1. A client posts transactions or calls the mock Plaid sync endpoint.
2. FastAPI validates request data and writes normalized records through
   SQLAlchemy.
3. Analytics endpoints query stored transactions and convert them into pandas
   DataFrames.
4. The analytics layer groups spending by category, merchant, and month.
5. The dashboard endpoint returns summary metrics for frontend consumption.

## Analytics Logic

- **Category summary:** Groups transaction amounts by category.
- **Merchant summary:** Aggregates spend by merchant.
- **Monthly summary:** Converts transaction dates into monthly trends.
- **Anomaly detection:** Flags unusually large transactions relative to the
  user's spending distribution.

## Design Tradeoffs

- SQLite is used by default for a fast local demo.
- The data model is PostgreSQL-ready through Docker Compose.
- Mock Plaid-style data keeps the project safe to run without external secrets.
- The analytics layer is separated from API routes so it can be tested directly.
