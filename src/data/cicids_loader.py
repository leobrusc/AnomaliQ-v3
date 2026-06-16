from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.data.synthetic import FEATURE_COLUMNS, generate_synthetic_http


CICIDS_HINT = (
    "CICIDS2017 não encontrado. Coloque os CSVs em data/raw/cicids2017/ "
    "com coluna de rótulo Label; o runner usará fallback sintético."
)


def load_cicids2017_binary(raw_dir: str = "data/raw/cicids2017", label_column: str = "Label", seed: int = 42) -> tuple[pd.DataFrame, str | None]:
    path = Path(raw_dir)
    csvs = sorted(path.glob("*.csv")) if path.exists() else []
    if not csvs:
        return generate_synthetic_http(seed=seed), CICIDS_HINT

    frames = []
    for csv in csvs:
        frame = pd.read_csv(csv, low_memory=False)
        if label_column in frame.columns:
            frames.append(frame)
    if not frames:
        return generate_synthetic_http(seed=seed), CICIDS_HINT

    df = pd.concat(frames, ignore_index=True)
    labels = df[label_column].astype(str).str.upper().str.strip()
    mask = labels.isin(["BENIGN", "DDOS", "DDoS".upper()])
    df = df.loc[mask].copy()
    df["label"] = (labels.loc[mask] != "BENIGN").astype(int)

    mapping = {
        "Flow Duration": "time_between_req_ms",
        "Total Fwd Packets": "req_per_sec",
        "Total Length of Fwd Packets": "payload_size_bytes",
        "Flow Bytes/s": "burst_score",
        "Flow Packets/s": "req_per_sec",
        "Bwd Packet Length Mean": "response_time_ms",
    }
    for source, target in mapping.items():
        if source in df.columns and target not in df.columns:
            df[target] = pd.to_numeric(df[source], errors="coerce")

    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
    df = df[FEATURE_COLUMNS + ["label"]].replace([float("inf"), float("-inf")], pd.NA).dropna()
    return df.sample(frac=1.0, random_state=seed).reset_index(drop=True), None
