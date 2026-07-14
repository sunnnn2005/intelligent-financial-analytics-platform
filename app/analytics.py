import numpy as np
import pandas as pd


def _frame(rows):
    return pd.DataFrame(rows)


def summarize_by_category(rows):
    if not rows:
        return []

    frame = _frame(rows)
    summary = (
        frame.groupby("category")
        .agg(total_spend=("amount", "sum"), transaction_count=("amount", "count"))
        .reset_index()
        .sort_values("total_spend", ascending=False)
    )

    return summary.to_dict(orient="records")


def summarize_by_merchant(rows):
    if not rows:
        return []

    frame = _frame(rows)
    summary = (
        frame.groupby("merchant_name")
        .agg(total_spend=("amount", "sum"), transaction_count=("amount", "count"))
        .reset_index()
        .sort_values("total_spend", ascending=False)
    )

    return summary.to_dict(orient="records")


def summarize_by_month(rows):
    if not rows:
        return []

    frame = _frame(rows)
    frame["month"] = pd.to_datetime(frame["transaction_date"]).dt.to_period("M").astype(str)
    summary = (
        frame.groupby("month")
        .agg(total_spend=("amount", "sum"), transaction_count=("amount", "count"))
        .reset_index()
        .sort_values("month")
    )

    return summary.to_dict(orient="records")


def detect_anomalies(rows):
    if len(rows) < 4:
        return []

    frame = _frame(rows)
    mean = frame["amount"].mean()
    std = frame["amount"].std(ddof=0)
    threshold = mean + (1.5 * std)

    if np.isnan(threshold):
        return []

    anomalies = frame[frame["amount"] > threshold].copy()
    anomalies["reason"] = anomalies["amount"].apply(
        lambda amount: f"Amount ${amount:.2f} is above the dynamic threshold ${threshold:.2f}"
    )

    return anomalies.to_dict(orient="records")


def build_dashboard_summary(rows):
    if not rows:
        return {
            "total_spend": 0,
            "transaction_count": 0,
            "top_category": None,
            "top_merchant": None,
            "anomaly_count": 0,
        }

    category_summary = summarize_by_category(rows)
    merchant_summary = summarize_by_merchant(rows)

    return {
        "total_spend": round(sum(row["amount"] for row in rows), 2),
        "transaction_count": len(rows),
        "top_category": category_summary[0]["category"] if category_summary else None,
        "top_merchant": merchant_summary[0]["merchant_name"] if merchant_summary else None,
        "anomaly_count": len(detect_anomalies(rows)),
    }
