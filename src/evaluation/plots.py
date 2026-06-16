from __future__ import annotations

import ast
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay


def ensure_plot_dir(output_dir: str) -> Path:
    path = Path(output_dir) / "plots"
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_bar(metrics_csv: str, column: str, title: str, filename: str):
    df = pd.read_csv(metrics_csv)
    if column not in df.columns or df.empty:
        return
    out = ensure_plot_dir(str(Path(metrics_csv).parent))
    data = df.dropna(subset=[column])
    if data.empty:
        return
    plt.figure(figsize=(10, 5))
    plt.bar(data["model"].astype(str), data[column].astype(float))
    plt.xticks(rotation=35, ha="right")
    plt.ylabel(column)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out / filename, dpi=160)
    plt.close()


def plot_confusion_matrix(row: dict, output_dir: str):
    cm = row.get("confusion_matrix")
    if isinstance(cm, str):
        cm = ast.literal_eval(cm)
    if not cm:
        return
    out = ensure_plot_dir(output_dir)
    ConfusionMatrixDisplay(np.asarray(cm), display_labels=["BENIGN", "DDoS"]).plot(values_format="d")
    plt.title(f"Matriz de confusão - {row.get('model', 'modelo')}")
    plt.tight_layout()
    plt.savefig(out / "confusion_matrix.png", dpi=160)
    plt.close()


def plot_series(values, output_dir: str, filename: str, title: str, ylabel: str):
    out = ensure_plot_dir(output_dir)
    plt.figure(figsize=(8, 4))
    plt.plot(list(values), marker="o")
    plt.title(title)
    plt.xlabel("iteração")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(out / filename, dpi=160)
    plt.close()


def plot_noise_degradation(df: pd.DataFrame, output_dir: str):
    if df.empty or "noise_level" not in df.columns:
        return
    out = ensure_plot_dir(output_dir)
    plt.figure(figsize=(7, 4))
    plt.plot(df["noise_level"], df["f1"], marker="o")
    plt.title("Degradação NISQ por ruído")
    plt.xlabel("nível de ruído")
    plt.ylabel("F1")
    plt.tight_layout()
    plt.savefig(out / "nisq_noise_degradation.png", dpi=160)
    plt.close()
