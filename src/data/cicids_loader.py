from __future__ import annotations

from pathlib import Path
import re
import pandas as pd

from src.data.synthetic import FEATURE_COLUMNS, generate_synthetic_http


CICIDS_HINT = (
    "CICIDS2017 não encontrado. Coloque os CSVs em data/raw/cicids2017/ "
    "com coluna de rótulo Label; o runner usará fallback sintético."
)
CICIDS_STRICT_MISSING = (
    "CICIDS2017 dataset not found.\n"
    "Expected CSV files under:\n"
    "data/raw/cicids2017/*.csv"
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


def load_cicids2017_binary(
    raw_dir: str = "data/raw/cicids2017",
    label_column: str = "Label",
    seed: int = 42,
    target_labels: list[str] | None = None,
    max_samples_per_class: int | None = None,
    processed_dir: str = "data/processed",
    fallback_to_synthetic: bool = True,
    require_real_dataset: bool = False,
) -> tuple[pd.DataFrame, str | None]:
    path = Path(raw_dir)
    csvs = sorted(path.glob("*.csv")) if path.exists() else []
    if not csvs:
        if require_real_dataset:
            raise FileNotFoundError(CICIDS_STRICT_MISSING)
        if fallback_to_synthetic:
            return generate_synthetic_http(seed=seed), CICIDS_HINT
        raise FileNotFoundError(CICIDS_STRICT_MISSING)

    frames = []
    for csv in csvs:
        frame = pd.read_csv(csv, low_memory=False)
        frame.columns = [_standardize_column(col) for col in frame.columns]
        normalized_label = _standardize_column(label_column)
        if normalized_label in frame.columns:
            frames.append(frame)
    if not frames:
        msg = f"CICIDS2017 encontrado em {raw_dir}, mas nenhuma coluna de rótulo '{label_column}' foi localizada."
        if fallback_to_synthetic:
            return generate_synthetic_http(seed=seed), msg
        raise ValueError(msg)

    df = pd.concat(frames, ignore_index=True)
    normalized_label = _standardize_column(label_column)
    labels = df[normalized_label].astype(str).str.upper().str.strip()
    allowed = [label.upper() for label in (target_labels or ["BENIGN", "DDOS", "DDOS"])]
    mask = labels.isin(allowed)
    df = df.loc[mask].copy()
    df["label"] = (labels.loc[mask] != "BENIGN").astype(int)

    mapping = {
        "flow_duration": "time_between_req_ms",
        "total_fwd_packets": "req_per_sec",
        "total_length_of_fwd_packets": "payload_size_bytes",
        "flow_bytes_s": "burst_score",
        "flow_packets_s": "req_per_sec",
        "bwd_packet_length_mean": "response_time_ms",
        "fwd_packet_length_mean": "payload_size_bytes",
        "fwd_iat_mean": "time_between_req_ms",
        "packet_length_std": "header_entropy",
        "destination_port": "distinct_endpoints_in_window",
        "init_win_bytes_forward": "source_ip_diversity",
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
    df.to_csv(out / "cicids2017_ddos_binary_processed.csv", index=False)
    return df, None
