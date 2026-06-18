from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

from src.experiments.common import load_config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/synthetic.yaml")
    parser.add_argument("--experiment-name", default="multiseed")
    parser.add_argument("--seeds", nargs="+", type=int, default=[42, 123, 2026])
    return parser.parse_args()


def main():
    args = parse_args()
    base_config = load_config(args.config)
    root = Path(base_config.get("experiments", {}).get("output_dir", "results"))
    temp_dir = root / "_multiseed_configs"
    temp_dir.mkdir(parents=True, exist_ok=True)
    run_dirs = []

    for seed in args.seeds:
        config = dict(base_config)
        config["seed"] = seed
        config_path = temp_dir / f"{Path(args.config).stem}_seed_{seed}.yaml"
        with open(config_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(config, fh, sort_keys=False, allow_unicode=True)
        name = f"{args.experiment_name}-seed-{seed}"
        subprocess.run(
            [sys.executable, "-m", "src.experiments.run_all", "--config", str(config_path), "--experiment-name", name],
            check=True,
        )
        dataset = config.get("dataset", {}).get("mode", "synthetic")
        candidates = sorted((root / dataset).glob(f"{name}-*"))
        if candidates:
            run_dirs.append(candidates[-1])

    rows = []
    for run_dir in run_dirs:
        metrics = run_dir / "metrics.csv"
        if metrics.exists():
            frame = pd.read_csv(metrics)
            frame["run_dir"] = str(run_dir)
            rows.append(frame)
    if not rows:
        return
    all_metrics = pd.concat(rows, ignore_index=True)
    summary = (
        all_metrics.groupby("model", dropna=False)
        .agg(
            f1_mean=("f1", "mean"),
            f1_std=("f1", "std"),
            roc_auc_mean=("roc_auc", "mean"),
            roc_auc_std=("roc_auc", "std"),
        )
        .reset_index()
    )
    out = root / base_config.get("dataset", {}).get("mode", "synthetic") / f"{args.experiment_name}-aggregate"
    out.mkdir(parents=True, exist_ok=True)
    all_metrics.to_csv(out / "multiseed_all_metrics.csv", index=False)
    summary.to_csv(out / "multiseed_summary.csv", index=False)


if __name__ == "__main__":
    main()
