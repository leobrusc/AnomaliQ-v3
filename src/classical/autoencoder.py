from __future__ import annotations

import time
import warnings

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPRegressor

from src.evaluation.metrics import alert_metrics, classification_metrics, merge_metrics


def run_classical_autoencoder(X_train, X_test, y_train, y_test, threshold_percentile: float = 95.0, seed: int = 42) -> dict:
    benign = X_train[y_train == 0]
    model = MLPRegressor(
        hidden_layer_sizes=(max(2, X_train.shape[1] // 2),),
        activation="relu",
        solver="adam",
        max_iter=300,
        random_state=seed,
        early_stopping=True,
    )
    start = time.perf_counter()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        model.fit(benign, benign)
    training_time = time.perf_counter() - start
    train_error = np.mean((benign - model.predict(benign)) ** 2, axis=1)
    threshold = np.percentile(train_error, threshold_percentile)
    start = time.perf_counter()
    error = np.mean((X_test - model.predict(X_test)) ** 2, axis=1)
    pred = (error >= threshold).astype(int)
    score = (error - error.min()) / max(error.max() - error.min(), 1e-9)
    inference_time = time.perf_counter() - start
    return merge_metrics(
        "Classical Autoencoder",
        classification_metrics(y_test, pred, score),
        alert_metrics(y_test, score, 0.5),
        {"training_time_seconds": training_time, "inference_time_seconds": inference_time, "final_loss": float(model.loss_)},
    )
