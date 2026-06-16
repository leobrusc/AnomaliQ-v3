from __future__ import annotations

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "response_time_ms",
    "req_per_sec",
    "http_status_code",
    "payload_size_bytes",
    "header_entropy",
    "distinct_endpoints_in_window",
    "time_between_req_ms",
    "ratio_4xx_5xx",
    "burst_score",
    "source_ip_diversity",
]


def generate_synthetic_http(n_samples: int = 600, attack_ratio: float = 0.35, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n_attack = int(n_samples * attack_ratio)
    n_benign = n_samples - n_attack

    benign = pd.DataFrame(
        {
            "response_time_ms": rng.normal(125, 38, n_benign).clip(20, None),
            "req_per_sec": rng.gamma(2.4, 2.4, n_benign),
            "http_status_code": rng.choice([200, 201, 204, 301, 404], n_benign, p=[0.68, 0.08, 0.08, 0.08, 0.08]),
            "payload_size_bytes": rng.normal(1150, 430, n_benign).clip(120, None),
            "header_entropy": rng.normal(3.95, 0.48, n_benign).clip(1.5, 6.4),
            "distinct_endpoints_in_window": rng.poisson(6, n_benign).clip(1, None),
            "time_between_req_ms": rng.normal(360, 150, n_benign).clip(25, None),
            "ratio_4xx_5xx": rng.beta(1.5, 10.0, n_benign),
            "burst_score": rng.beta(1.7, 7.0, n_benign),
            "source_ip_diversity": rng.normal(0.67, 0.15, n_benign).clip(0.08, 1.0),
            "label": 0,
        }
    )

    n_low = max(1, int(n_attack * 0.28))
    n_flood = n_attack - n_low
    flood = pd.DataFrame(
        {
            "response_time_ms": rng.normal(285, 95, n_flood).clip(55, None),
            "req_per_sec": rng.gamma(7.0, 4.8, n_flood),
            "http_status_code": rng.choice([200, 403, 404, 429, 500, 503], n_flood, p=[0.22, 0.12, 0.18, 0.22, 0.12, 0.14]),
            "payload_size_bytes": rng.normal(520, 240, n_flood).clip(45, None),
            "header_entropy": rng.normal(4.95, 0.65, n_flood).clip(2.0, 7.5),
            "distinct_endpoints_in_window": rng.poisson(15, n_flood).clip(2, None),
            "time_between_req_ms": rng.normal(62, 35, n_flood).clip(2, None),
            "ratio_4xx_5xx": rng.beta(4.3, 2.6, n_flood),
            "burst_score": rng.beta(6.0, 2.0, n_flood),
            "source_ip_diversity": rng.normal(0.34, 0.14, n_flood).clip(0.02, 0.9),
            "label": 1,
        }
    )
    low_and_slow = pd.DataFrame(
        {
            "response_time_ms": rng.normal(170, 55, n_low).clip(40, None),
            "req_per_sec": rng.gamma(3.2, 2.8, n_low),
            "http_status_code": rng.choice([200, 301, 403, 404, 429, 500], n_low, p=[0.42, 0.05, 0.1, 0.18, 0.18, 0.07]),
            "payload_size_bytes": rng.normal(820, 320, n_low).clip(80, None),
            "header_entropy": rng.normal(4.45, 0.55, n_low).clip(2.0, 7.2),
            "distinct_endpoints_in_window": rng.poisson(9, n_low).clip(2, None),
            "time_between_req_ms": rng.normal(170, 80, n_low).clip(10, None),
            "ratio_4xx_5xx": rng.beta(2.8, 4.0, n_low),
            "burst_score": rng.beta(3.5, 3.8, n_low),
            "source_ip_diversity": rng.normal(0.48, 0.16, n_low).clip(0.04, 0.95),
            "label": 1,
        }
    )
    attack = pd.concat([flood, low_and_slow], ignore_index=True)

    df = pd.concat([benign, attack], ignore_index=True)
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    df["timestamp"] = pd.date_range("2026-01-01", periods=len(df), freq="s")
    return df
