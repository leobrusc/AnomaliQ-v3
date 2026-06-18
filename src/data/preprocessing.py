from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from src.data.cicids_loader import load_cicids2017_binary
from src.data.synthetic import FEATURE_COLUMNS, generate_synthetic_http
from src.data.unsw_loader import load_unsw_nb15_binary


def load_dataset(config: dict) -> tuple[pd.DataFrame, list[str]]:
    seed = int(config.get("seed", 42))
    dataset = config.get("dataset", {})
    mode = dataset.get("mode", "synthetic")
    warnings: list[str] = []
    if mode == "cicids2017":
        cicids = dataset.get("cicids", {})
        df, warning = load_cicids2017_binary(
            raw_dir=cicids.get("raw_dir", "data/raw/cicids2017"),
            label_column=cicids.get("label_column", "Label"),
            seed=seed,
            target_labels=cicids.get("target_labels", ["BENIGN", "DDoS"]),
            max_samples_per_class=cicids.get("max_samples_per_class"),
            processed_dir=cicids.get("processed_dir", "data/processed"),
            fallback_to_synthetic=bool(cicids.get("fallback_to_synthetic", True)),
        )
        if warning:
            warnings.append(warning)
        return df, warnings
    if mode == "unsw_nb15":
        unsw = dataset.get("unsw", {})
        df, warning = load_unsw_nb15_binary(
            raw_dir=unsw.get("raw_dir", "data/raw/unsw_nb15"),
            label_column=unsw.get("label_column", "label"),
            seed=seed,
            max_samples_per_class=unsw.get("max_samples_per_class"),
            processed_dir=unsw.get("processed_dir", "data/processed"),
            fallback_to_synthetic=bool(unsw.get("fallback_to_synthetic", True)),
        )
        if warning:
            warnings.append(warning)
        return df, warnings

    synthetic = dataset.get("synthetic", {})
    return generate_synthetic_http(
        n_samples=int(synthetic.get("n_samples", 600)),
        attack_ratio=float(synthetic.get("attack_ratio", 0.35)),
        seed=seed,
    ), warnings


def make_splits(config: dict):
    df, warnings = load_dataset(config)
    X = df[FEATURE_COLUMNS].astype(float)
    y = df["label"].astype(int).to_numpy()
    pre = config.get("preprocessing", {})
    return (*train_test_split(X, y, test_size=float(pre.get("test_size", 0.3)), random_state=int(config.get("seed", 42)), stratify=y), warnings)


def scale_classical(X_train: pd.DataFrame, X_test: pd.DataFrame):
    scaler = StandardScaler()
    return scaler.fit_transform(X_train), scaler.transform(X_test), scaler


def reduce_for_quantum(X_train: pd.DataFrame, X_test: pd.DataFrame, n_qubits: int):
    scaler = StandardScaler()
    pca = PCA(n_components=n_qubits, random_state=42)
    X_train_pca = pca.fit_transform(scaler.fit_transform(X_train))
    X_test_pca = pca.transform(scaler.transform(X_test))
    angle_scaler = MinMaxScaler(feature_range=(0.0, np.pi))
    return angle_scaler.fit_transform(X_train_pca), angle_scaler.transform(X_test_pca), scaler, pca, angle_scaler


def limit_quantum_samples(X_train, X_test, y_train, y_test, max_train: int, max_test: int, seed: int = 42):
    rng = np.random.default_rng(seed)

    def pick(X, y, n):
        n = min(n, len(y))
        idx = rng.choice(np.arange(len(y)), size=n, replace=False)
        return X[idx], y[idx]

    return (*pick(X_train, y_train, max_train), *pick(X_test, y_test, max_test))
