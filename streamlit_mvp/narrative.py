from __future__ import annotations

import os
import requests
import pandas as pd
from analytics import correlation_table, rolling_summary


def generate_narrative(df: pd.DataFrame) -> str:
    if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_BASE_URL"):
        try:
            return _openai_narrative(df)
        except requests.RequestException:
            pass
    return _fallback_narrative(df)


def _openai_narrative(df: pd.DataFrame) -> str:
    base = os.getenv("OPENAI_BASE_URL", "").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Write privacy-preserving neuroscience-informed cognitive performance summaries. Avoid diagnosis."},
            {"role": "user", "content": df.tail(20).to_json(orient="records")},
        ],
        "temperature": 0.4,
    }
    resp = requests.post(f"{base}/v1/chat/completions", json=payload, headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}, timeout=20)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _fallback_narrative(df: pd.DataFrame) -> str:
    if df.empty:
        return "Add a cognitive session to generate a personalized narrative."
    corr = correlation_table(df)
    summary = rolling_summary(df)
    recent = df.tail(6)
    latest = df.iloc[-1]
    sleep_memory = corr.loc["sleep_quality", "digit_span"] if {"sleep_quality", "digit_span"}.issubset(corr.index) else 0
    stress_rt = corr.loc["stress", "reaction_time_ms"] if {"stress", "reaction_time_ms"}.issubset(corr.index) else 0
    alert_stroop = corr.loc["alertness", "stroop_accuracy"] if {"alertness", "stroop_accuracy"}.issubset(corr.index) else 0
    cei_delta = summary.get("cei_delta", 0)
    direction = "improved" if cei_delta > 1 else "softened" if cei_delta < -1 else "remained stable"
    variants = [
        "Your recent profile suggests the prefrontal working-memory system is most responsive to recovery state.",
        "The current pattern looks like a resource-allocation story: speed, inhibition, and subjective energy are moving together.",
        "Across sessions, the strongest signal is not a single score but the coupling among sleep, stress, and executive control.",
    ]
    opener = variants[int(abs(hash(str(latest.get('date')))) % len(variants))]
    return (
        f"{opener} Over the latest rolling window, your Cognitive Efficiency Index {direction} "
        f"by {cei_delta:+.1f} points. The latest CEI is {latest.get('cei', 0):.1f}. "
        f"Sleep and digit span show a correlation of {sleep_memory:+.2f}, consistent with hippocampal-prefrontal networks benefiting from recovery. "
        f"Stress and reaction time correlate at {stress_rt:+.2f}; positive values indicate sympathetic arousal may be slowing response selection. "
        f"Alertness and Stroop accuracy correlate at {alert_stroop:+.2f}, a useful marker for executive inhibition. "
        f"In the last {len(recent)} sessions, average reaction time was {recent['reaction_time_ms'].mean():.0f} ms and Stroop accuracy was {recent['stroop_accuracy'].mean():.0%}. "
        "This is an educational analytics summary, not a medical diagnosis."
    )
