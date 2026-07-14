import numpy as np
import pandas as pd


def summarize_by_category(rows):
    if not rows:
        return []

    frame = pd.DataFrame(rows)
    summary = (
        frame.groupby("category")
        .agg(total_spend=("amount", "sum"), transaction_count=("amount", "count"))
        .reset_index()
        .sort_values("total_spend", ascending=False)
    )

    return summary.to_dict(orient="records")


def detect_anomalies(rows):
    if len(rows) < 4:
        return []

    frame = pd.DataFrame(rows)
    mean = frame["amount"].mean()
    std = frame["amount"].std(ddof=0)
    threshold = mean + (2 * std)

    if np.isnan(threshold):
        return []

    anomalies = frame[frame["amount"] > threshold].copy()
    anomalies["reason"] = anomalies["amount"].apply(
        lambda amount: f"Amount ${amount:.2f} is above the dynamic threshold ${threshold:.2f}"
    )

    return anomalies.to_dict(orient="records")
