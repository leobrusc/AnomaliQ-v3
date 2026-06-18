from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

from src.data.synthetic import FEATURE_COLUMNS, generate_synthetic_http


UNSW_HINT = (
    "UNSW-NB15 não encontrado. Coloque os CSVs em data/raw/unsw_nb15/ "
    "com coluna 'label' binária ou 'attack_cat'."
)


def _standardize_column(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def _limit_per_class(df: pd.DataFrame, max_samples_per_class: int | None, seed: int) -> pd.DataFrame:
    if not max_samples_per_class:
        return df
    return (
        df.groupby("label", group_keys=False)
        .apply(lambda part: part.sample(n=min(len(part), max_samples_per_class), random_state=seed))
        .sample(frac=1.0, random_state=seed)
        .reset_index(drop=True)
    )


def load_unsw_nb15_binary(
    raw_dir: str = "data/raw/unsw_nb15",
    label_column: str = "label",
    seed: int = 42,
    max_samples_per_class: int | None = None,
    processed_dir: str = "data/processed",
    fallback_to_synthetic: bool = True,
) -> tuple[pd.DataFrame, str | None]:
    path = Path(raw_dir)
    csvs = sorted(path.glob("*.csv")) if path.exists() else []
    if not csvs:
        if fallback_to_synthetic:
            return generate_synthetic_http(seed=seed), UNSW_HINT
        raise FileNotFoundError(UNSW_HINT)

    frames = []
    for csv in csvs:
        frame = pd.read_csv(csv, low_memory=False)
        frame.columns = [_standardize_column(col) for col in frame.columns]
        frames.append(frame)
    df = pd.concat(frames, ignore_index=True)

    normalized_label = _standardize_column(label_column)
    if normalized_label in df.columns:
        raw_label = df[normalized_label]
        if raw_label.dtype == object:
            labels = raw_label.astype(str).str.upper().str.strip()
            df["label"] = (~labels.isin(["0", "NORMAL", "BENIGN"])).astype(int)
        else:
            df["label"] = pd.to_numeric(raw_label, errors="coerce").fillna(1).astype(int).clip(0, 1)
    elif "attack_cat" in df.columns:
        labels = df["attack_cat"].astype(str).str.upper().str.strip()
        df["label"] = (~labels.isin(["NORMAL", "BENIGN"])).astype(int)
    else:
        msg = "UNSW-NB15 encontrado, mas nenhuma coluna 'label' ou 'attack_cat' foi localizada."
        if fallback_to_synthetic:
            return generate_synthetic_http(seed=seed), msg
        raise ValueError(msg)

    for col in df.select_dtypes(include=["object", "category"]).columns:
        if col != "attack_cat":
            df[col] = pd.factorize(df[col].astype(str), sort=True)[0]

    mapping = {
        "dur": "time_between_req_ms",
        "rate": "req_per_sec",
        "sbytes": "payload_size_bytes",
        "dbytes": "response_time_ms",
        "sttl": "header_entropy",
        "ct_dst_sport_ltm": "distinct_endpoints_in_window",
        "sload": "burst_score",
        "dload": "source_ip_diversity",
        "ct_state_ttl": "ratio_4xx_5xx",
        "service": "http_status_code",
    }
    for source, target in mapping.items():
        if source in df.columns:
            df[target] = pd.to_numeric(df[source], errors="coerce")

    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
    df = df[FEATURE_COLUMNS + ["label"]].apply(pd.to_numeric, errors="coerce").replace([float("inf"), float("-inf")], pd.NA).dropna()
    df = _limit_per_class(df, max_samples_per_class, seed)
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    out = Path(processed_dir)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "unsw_nb15_binary_processed.csv", index=False)
    return df, None
