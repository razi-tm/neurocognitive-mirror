from __future__ import annotations
import numpy as np
import pandas as pd
from app.schemas.payloads import SessionPayload

def frame(sessions: list[SessionPayload]) -> pd.DataFrame:
    df = pd.DataFrame([s.model_dump() for s in sessions])
    df["session_date"] = pd.to_datetime(df["session_date"].fillna(pd.Timestamp.utcnow()))
    return df.sort_values("session_date")

def cei(df: pd.DataFrame) -> pd.Series:
    higher = ["digit_span", "stroop_accuracy", "alertness", "sleep_quality"]
    lower = ["reaction_time_ms", "stroop_interference_ms", "stress"]
    zs = []
    for c in higher + lower:
        x = df[c].astype(float); std = x.std(ddof=0) or 1
        z = (x - x.mean()) / std
        zs.append(z if c in higher else -z)
    return (50 + 10 * pd.concat(zs, axis=1).mean(axis=1)).clip(0, 100)

def analyze_sessions(sessions: list[SessionPayload]) -> dict:
    df = frame(sessions)
    df["cei"] = cei(df)
    corr = df[["sleep_quality","stress","alertness","digit_span","reaction_time_ms","stroop_accuracy","stroop_interference_ms","cei"]].corr(numeric_only=True).fillna(0)
    return {
        "latest": df.tail(1).to_dict("records")[0],
        "correlations": corr.round(3).to_dict(),
        "rolling": df[["session_date","cei","digit_span","reaction_time_ms","stroop_accuracy"]].rolling(4, min_periods=1).mean(numeric_only=True).round(3).to_dict("records"),
        "domain_scores": {
            "working_memory": float(np.clip(df["digit_span"].iloc[-1] / 12 * 100, 0, 100)),
            "processing_speed": float(np.clip(100 - (df["reaction_time_ms"].iloc[-1] - 180) / 5, 0, 100)),
            "executive_control": float(np.clip(df["stroop_accuracy"].iloc[-1] * 100 - df["stroop_interference_ms"].iloc[-1] / 10, 0, 100)),
        },
    }
