from __future__ import annotations

from src.classical.autoencoder import run_classical_autoencoder


def run_qae_placeholder(X_train, X_test, y_train, y_test, seed: int = 42) -> dict:
    row = run_classical_autoencoder(X_train, X_test, y_train, y_test, seed=seed)
    row["model"] = "QAE interface (classical AE fallback)"
    row["qae_status"] = "TODO: substituir MLPRegressor por ansatz QAE quando runtime variacional estiver disponível."
    return row
