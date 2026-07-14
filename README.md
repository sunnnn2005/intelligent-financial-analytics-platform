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
- Seed endpoint for mock Plaid-style transactions
- Category-level monthly spending summary
- Simple anomaly detection for unusually large transactions
- Clean API structure for future dashboard integration

## Resume Bullets

- Developed a backend analytics platform that ingests transaction data, normalizes
  financial records, and stores structured user spending data with SQLAlchemy.
- Implemented transaction cleaning and category-mapping workflows with pandas and
  NumPy to analyze monthly spending patterns across merchants and categories.
- Built REST API endpoints for spending summaries, anomaly detection, and
  category-level insights, enabling dashboard-ready financial reporting.

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Project Roadmap

- Replace mock data with Plaid Sandbox integration
- Add PostgreSQL Docker Compose setup
- Add React dashboard
- Add user authentication
- Add recurring subscription detection
- Add tests for categorization and anomaly detection
