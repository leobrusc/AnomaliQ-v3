from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


CLASSIFICATION_COLUMNS = ["accuracy", "precision", "recall", "f1", "roc_auc", "mcc"]
TIMING_COLUMNS = ["training_time_seconds", "inference_time_seconds"]
NISQ_COLUMNS = ["n_qubits", "circuit_depth", "num_parameters", "cx_count"]


def _format_metric(mean_value, std_value) -> str:
    if pd.isna(mean_value):
        return ""
    if pd.isna(std_value):
        return f"{mean_value:.4f}"
    return f"{mean_value:.4f} ± {std_value:.4f}"


def aggregate_publication_metrics(metrics: pd.DataFrame, models: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = metrics[metrics["model"].isin(models)].copy()
    data["model"] = pd.Categorical(data["model"], categories=models, ordered=True)
    data = data.sort_values(["model"])
    metric_cols = [col for col in CLASSIFICATION_COLUMNS + TIMING_COLUMNS + NISQ_COLUMNS if col in data.columns]
    summary = data.groupby("model", observed=False)[metric_cols].agg(["mean", "std"]).reset_index()
    summary.columns = ["_".join([part for part in col if part]).strip("_") if isinstance(col, tuple) else col for col in summary.columns]
    table = pd.DataFrame({"model": summary["model"].astype(str)})
    for col in CLASSIFICATION_COLUMNS:
        mean_col = f"{col}_mean"
        std_col = f"{col}_std"
        if mean_col in summary.columns:
            table[col] = [_format_metric(mean, std) for mean, std in zip(summary[mean_col], summary.get(std_col, pd.Series([pd.NA] * len(summary))))]
    return data, table


def write_publication_tables(metrics: pd.DataFrame, output_dir: str, models: list[str]) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw, table = aggregate_publication_metrics(metrics, models)
    raw_path = out / "cicids2017_selected_model_metrics.csv"
    summary_path = out / "cicids2017_publication_summary.csv"
    md_path = out / "cicids2017_publication_table.md"
    tex_path = out / "cicids2017_publication_table.tex"
    raw.to_csv(raw_path, index=False)
    table.to_csv(summary_path, index=False)
    try:
        md = table.to_markdown(index=False)
    except Exception:
        md = table.to_string(index=False)
    md_path.write_text(md + "\n", encoding="utf-8")
    tex_path.write_text(table.to_latex(index=False, escape=True), encoding="utf-8")
    return {"raw": raw_path, "summary": summary_path, "markdown": md_path, "latex": tex_path}


def _plot_metric(summary: pd.DataFrame, metric: str, output_dir: str):
    mean_col = f"{metric}_mean"
    std_col = f"{metric}_std"
    if mean_col not in summary.columns:
        return
    data = summary.dropna(subset=[mean_col])
    if data.empty:
        return
    out = Path(output_dir) / "plots"
    out.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 4.8))
    yerr = data[std_col] if std_col in data.columns else None
    plt.bar(data["model"].astype(str), data[mean_col], yerr=yerr, capsize=4)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel(metric.upper())
    plt.title(f"CICIDS2017 BENIGN vs DDoS - {metric.upper()} by model")
    plt.tight_layout()
    plt.savefig(out / f"cicids2017_{metric}_publication.png", dpi=220)
    plt.close()


def write_publication_figures(metrics: pd.DataFrame, output_dir: str, models: list[str]) -> list[Path]:
    data = metrics[metrics["model"].isin(models)].copy()
    data["model"] = pd.Categorical(data["model"], categories=models, ordered=True)
    metric_cols = [col for col in CLASSIFICATION_COLUMNS + TIMING_COLUMNS + NISQ_COLUMNS if col in data.columns]
    summary = data.groupby("model", observed=False)[metric_cols].agg(["mean", "std"]).reset_index()
    summary.columns = ["_".join([part for part in col if part]).strip("_") if isinstance(col, tuple) else col for col in summary.columns]
    before = set((Path(output_dir) / "plots").glob("*.png")) if (Path(output_dir) / "plots").exists() else set()
    for metric in ["accuracy", "precision", "recall", "f1", "roc_auc", "mcc"]:
        _plot_metric(summary, metric, output_dir)
    after = set((Path(output_dir) / "plots").glob("*.png")) if (Path(output_dir) / "plots").exists() else set()
    return sorted(after - before)
