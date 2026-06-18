from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from src.data.preprocessing import limit_quantum_samples, make_splits, reduce_for_quantum, scale_classical
from src.evaluation.plots import plot_bar, plot_confusion_matrix
from src.evaluation.reproducibility import initialize_experiment
from src.evaluation.reports import append_rows, record_failure, write_summary


def enforce_required_real_dataset(config: dict):
    dataset = config.get("dataset", {})
    mode = dataset.get("mode", "synthetic")
    if mode == "cicids2017":
        cicids = dataset.get("cicids", {})
        if bool(cicids.get("require_real_dataset", False)):
            raw_dir = cicids.get("raw_dir", "data/raw/cicids2017")
            if not list(Path(raw_dir).rglob("*.csv")):
                raise FileNotFoundError(
                    "CICIDS2017 dataset not found.\n"
                    "Expected CSV files under:\n"
                    "data/raw/cicids2017/*.csv"
                )
    if mode == "unsw_nb15":
        unsw = dataset.get("unsw", {})
        if bool(unsw.get("require_real_dataset", False)):
            raw_dir = unsw.get("raw_dir", "data/raw/unsw_nb15")
            if not list(Path(raw_dir).glob("*.csv")):
                raise FileNotFoundError(
                    "UNSW-NB15 dataset not found.\n"
                    "Expected CSV files under:\n"
                    "data/raw/unsw_nb15/*.csv"
                )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/synthetic.yaml")
    parser.add_argument("--experiment-name", default=None)
    parser.add_argument("--reset", action="store_true")
    return parser.parse_args()


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def output_dir(config: dict) -> str:
    if "_experiment" in config:
        out = config["_experiment"]["output_dir"]
        Path(out, "plots").mkdir(parents=True, exist_ok=True)
        Path(out, "artifacts").mkdir(parents=True, exist_ok=True)
        return out
    out = config.get("experiments", {}).get("output_dir", "results")
    Path(out, "plots").mkdir(parents=True, exist_ok=True)
    Path(out, "artifacts").mkdir(parents=True, exist_ok=True)
    return out


def load_and_initialize(args) -> dict:
    config = load_config(args.config)
    return initialize_experiment(config, args.config, args.experiment_name)


def reset_outputs(out: str):
    for name in ["metrics.csv", "failures.csv", "summary.md"]:
        path = Path(out) / name
        if path.exists():
            path.unlink()


def prepared_classical(config: dict):
    X_train, X_test, y_train, y_test, warnings = make_splits(config)
    Xtr, Xte, _ = scale_classical(X_train, X_test)
    return Xtr, Xte, y_train, y_test, warnings


def prepared_quantum(config: dict):
    X_train, X_test, y_train, y_test, warnings = make_splits(config)
    pre = config.get("preprocessing", {})
    Xtr, Xte, *_ = reduce_for_quantum(X_train, X_test, int(pre.get("n_qubits", 4)))
    return (*limit_quantum_samples(Xtr, Xte, y_train, y_test, int(pre.get("quantum_max_train", 80)), int(pre.get("quantum_max_test", 60)), int(config.get("seed", 42))), warnings)


def finish(out: str, warnings: list[str] | None = None):
    metrics = Path(out) / "metrics.csv"
    if metrics.exists():
        plot_bar(str(metrics), "f1", "Comparação F1 por modelo", "f1_comparison.png")
        plot_bar(str(metrics), "roc_auc", "Comparação ROC-AUC por modelo", "roc_auc_comparison.png")
        import pandas as pd

        df = pd.read_csv(metrics)
        if not df.empty and "confusion_matrix" in df.columns:
            candidates = df.dropna(subset=["f1", "confusion_matrix"])
            candidates = candidates[candidates["confusion_matrix"].astype(str).str.startswith("[[")]
            if not candidates.empty:
                best = candidates.sort_values("f1", ascending=False).iloc[0].to_dict()
                plot_confusion_matrix(best, out)
    write_summary(out, warnings or [])


def run_and_record(config: dict, experiment: str, fn):
    out = output_dir(config)
    try:
        rows, warnings = fn(config)
        if rows:
            append_rows(out, rows if isinstance(rows, list) else [rows])
        return warnings
    except Exception as exc:
        record_failure(out, experiment, repr(exc))
        return []
