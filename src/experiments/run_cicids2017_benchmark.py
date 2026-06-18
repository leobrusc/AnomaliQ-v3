from __future__ import annotations

import argparse
import sys
from copy import deepcopy
from pathlib import Path

import pandas as pd

from src.classical.baselines import run_classical_baselines
from src.evaluation.publication import write_publication_figures, write_publication_tables
from src.evaluation.reports import append_rows, write_summary
from src.evaluation.reproducibility import initialize_experiment
from src.experiments.common import enforce_required_real_dataset, load_config, output_dir, prepared_classical, prepared_quantum
from src.quantum.qsvm import run_qsvm
from src.quantum.vqc import run_vqc


SELECTED_MODELS = ["Logistic Regression", "Random Forest", "SVM-RBF", "QSVM-ZZ", "QSVM-PAULI", "VQC"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/cicids_ddos_real_strict.yaml")
    parser.add_argument("--experiment-name", default="cicids2017_real_benchmark")
    parser.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 2026])
    return parser.parse_args()


def run_selected_models(config: dict) -> list[dict]:
    exp = config.get("experiments", {})
    threshold = float(exp.get("alert_threshold", 0.5))
    seed = int(config.get("seed", 42))
    rows: list[dict] = []

    X_train, X_test, y_train, y_test, _ = prepared_classical(config)
    classical_rows = run_classical_baselines(X_train, X_test, y_train, y_test, threshold, seed)
    rows.extend(row for row in classical_rows if row.get("model") in {"Logistic Regression", "Random Forest", "SVM-RBF"})

    Xq_train, yq_train, Xq_test, yq_test, _ = prepared_quantum(config)
    n_qubits = int(config.get("preprocessing", {}).get("n_qubits", 4))
    for map_type in ["zz", "pauli"]:
        rows.append(run_qsvm(Xq_train, Xq_test, yq_train, yq_test, n_qubits, map_type, threshold, seed))
    rows.append(
        run_vqc(
            Xq_train,
            Xq_test,
            yq_train,
            yq_test,
            n_qubits,
            int(exp.get("vqc_maxiter", 25)),
            output_dir(config),
            threshold,
            seed,
        )
    )
    return rows


def main():
    args = parse_args()
    base_config = load_config(args.config)
    try:
        enforce_required_real_dataset(base_config)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from None
    run_dirs = []

    for seed in args.seeds:
        config = deepcopy(base_config)
        config["seed"] = seed
        config = initialize_experiment(config, args.config, f"{args.experiment_name}-seed-{seed}")
        out = output_dir(config)
        rows = run_selected_models(config)
        append_rows(out, rows)
        write_summary(out, [])
        run_dirs.append(Path(out))

    frames = []
    for run_dir in run_dirs:
        metrics = run_dir / "metrics.csv"
        if metrics.exists():
            frame = pd.read_csv(metrics)
            frame["run_dir"] = str(run_dir)
            frames.append(frame)
    if not frames:
        return

    all_metrics = pd.concat(frames, ignore_index=True)
    root = Path(base_config.get("experiments", {}).get("output_dir", "results"))
    aggregate_dir = root / "cicids2017" / f"{args.experiment_name}-aggregate"
    aggregate_dir.mkdir(parents=True, exist_ok=True)
    all_metrics.to_csv(aggregate_dir / "cicids2017_multiseed_all_metrics.csv", index=False)
    write_publication_tables(all_metrics, str(aggregate_dir), SELECTED_MODELS)
    write_publication_figures(all_metrics, str(aggregate_dir), SELECTED_MODELS)


if __name__ == "__main__":
    main()
