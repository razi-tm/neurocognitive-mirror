from __future__ import annotations

from datetime import date, timedelta
import numpy as np
import pandas as pd


def generate_demo_data(seed: int = 42, weeks: int = 104) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    today = date.today()
    start = today - timedelta(weeks=weeks - 1)
    rows = []
    baseline_memory = 7.2
    baseline_rt = 285.0
    baseline_stroop = 0.82
    for i in range(weeks):
        d = start + timedelta(weeks=i)
        seasonal = np.sin(i / 52 * 2 * np.pi)
        fatigue = 0.6 * np.sin(i / 8 * 2 * np.pi) + rng.normal(0, 0.25)
        recovery = 0.4 * np.cos(i / 5 * 2 * np.pi)
        sleep = float(np.clip(7.1 + 0.45 * seasonal + recovery - 0.35 * fatigue + rng.normal(0, 0.55), 3.5, 9.8))
        stress = float(np.clip(4.2 + 1.4 * fatigue - 0.45 * seasonal + rng.normal(0, 1.0), 1, 10))
        alertness = float(np.clip(5.6 + 0.75 * (sleep - 7) - 0.35 * stress + recovery + rng.normal(0, 0.75), 1, 10))
        digit_span = int(np.clip(round(baseline_memory + 0.42 * (sleep - 7) + 0.18 * alertness - 0.18 * stress + rng.normal(0, 0.75)), 3, 12))
        reaction_time_ms = float(np.clip(baseline_rt - 4.8 * alertness + 8.5 * stress - 7.5 * (sleep - 7) + rng.normal(0, 24), 170, 620))
        stroop_accuracy = float(np.clip(baseline_stroop + 0.018 * alertness - 0.017 * stress + 0.011 * (sleep - 7) + rng.normal(0, 0.045), 0.45, 0.99))
        stroop_interference_ms = float(np.clip(120 + 10 * stress - 8 * alertness + rng.normal(0, 22), 35, 310))
        rows.append({
            "date": d.isoformat(),
            "sleep_quality": round(sleep, 2),
            "stress": round(stress, 2),
            "alertness": round(alertness, 2),
            "digit_span": digit_span,
            "reaction_time_ms": round(reaction_time_ms, 1),
            "stroop_accuracy": round(stroop_accuracy, 3),
            "stroop_interference_ms": round(stroop_interference_ms, 1),
            "notes": "synthetic demo observation",
            "source": "demo",
        })
    return pd.DataFrame(rows)
