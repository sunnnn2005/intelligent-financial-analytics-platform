# Intelligent Financial Analytics Platform

A personal finance analytics backend that ingests transaction data, cleans and
categorizes transactions, and exposes API endpoints for dashboard-ready spending
insights.

## Why This Project

This project is useful for software engineering, data analyst, and data science
internships because it combines API design, database modeling, data cleaning,
and product analytics.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL-ready data model
- pandas + NumPy
- Plaid Sandbox-inspired mock data

## MVP Features

- Transaction ingestion endpoint
- Mock Plaid sync endpoint for sandbox-style transactions
- Category, merchant, and monthly spending summaries
- Simple anomaly detection for unusually large transactions
- Dashboard summary endpoint for frontend-ready metrics
- Lightweight local dashboard at `/dashboard`
- Isolated test suite for analytics and API behavior

## Resume Bullets

- Developed a backend analytics platform that ingests transaction data, normalizes
  financial records, and stores structured user spending data with SQLAlchemy.
- Implemented transaction cleaning and category-mapping workflows with pandas and
  NumPy to analyze monthly spending patterns across merchants and categories.
- Built REST API endpoints for spending summaries, anomaly detection, and
  category-level insights, enabling dashboard-ready financial reporting.

## Local Run

Recommended Python version: `3.12`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Dashboard: http://localhost:8000/dashboard

Seed demo data:

```bash
curl -X POST http://localhost:8000/seed
```

Run tests:

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## API Endpoints

- `POST /transactions` creates a transaction
- `POST /plaid/sync/mock` syncs Plaid Sandbox-inspired mock transactions
- `POST /seed` loads Plaid Sandbox-inspired mock transactions
- `GET /transactions` lists transactions
- `GET /analytics/category-summary` groups spend by category
- `GET /analytics/merchant-summary` groups spend by merchant
- `GET /analytics/monthly-summary` groups spend by month
- `GET /analytics/anomalies` flags unusually large transactions
- `GET /analytics/dashboard` returns dashboard-ready metrics

## Environment Notes

The data stack is pinned for Python 3.12 because pandas and NumPy wheels are
more reliable there than on bleeding-edge Python versions. If your default
`python3` is newer, create the virtual environment with a Python 3.12 binary.

The default local database is SQLite. To run with PostgreSQL:

```bash
docker compose up --build
curl -X POST http://localhost:8000/plaid/sync/mock
```

The Docker Compose setup uses a local Postgres container and does not require
paid Plaid credentials.

## Project Roadmap

- Replace mock data with Plaid Sandbox integration
- Add user authentication
- Add recurring subscription detection
- Add React dashboard
