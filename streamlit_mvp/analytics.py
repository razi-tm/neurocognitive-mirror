from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

METRICS = ["digit_span", "reaction_time_ms", "stroop_accuracy", "stroop_interference_ms", "sleep_quality", "stress", "alertness"]


def prepare_frame(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if data.empty:
        return data
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")
    for metric in METRICS:
        if metric in data:
            data[metric] = pd.to_numeric(data[metric], errors="coerce")
    data["cei"] = cognitive_efficiency_index(data)
    for metric in ["digit_span", "reaction_time_ms", "stroop_accuracy", "cei"]:
        if metric in data:
            data[f"{metric}_ma4"] = data[metric].rolling(4, min_periods=1).mean()
    return data


def cognitive_efficiency_index(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=float)
    higher = ["digit_span", "stroop_accuracy", "alertness", "sleep_quality"]
    lower = ["reaction_time_ms", "stroop_interference_ms", "stress"]
    scores = []
    for col in higher + lower:
        x = pd.to_numeric(df[col], errors="coerce")
        std = x.std(ddof=0) or 1.0
        z = (x - x.mean()) / std
        scores.append(z if col in higher else -z)
    cei = 50 + 10 * pd.concat(scores, axis=1).mean(axis=1)
    return cei.clip(0, 100).round(1)


def correlation_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in METRICS + ["cei"] if c in df]
    return df[cols].corr(numeric_only=True).round(3)


def outliers(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    if df.empty or metric not in df:
        return pd.DataFrame()
    z = np.abs(stats.zscore(df[metric].dropna(), nan_policy="omit"))
    idx = df[metric].dropna().index[z > 2.0]
    return df.loc[idx, ["date", metric, "notes"]]


def rolling_summary(df: pd.DataFrame, window: int = 4) -> dict[str, float]:
    if df.empty:
        return {}
    recent = df.tail(window)
    previous = df.iloc[max(0, len(df) - 2 * window): max(0, len(df) - window)]
    summary: dict[str, float] = {}
    for col in ["cei", "digit_span", "reaction_time_ms", "stroop_accuracy"]:
        if col in recent and not previous.empty:
            summary[f"{col}_delta"] = float(recent[col].mean() - previous[col].mean())
        elif col in recent:
            summary[f"{col}_delta"] = 0.0
    return summary
