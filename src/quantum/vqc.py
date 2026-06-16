from __future__ import annotations

import time
import warnings
import logging

import numpy as np
from qiskit.circuit.library import RealAmplitudes
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPClassifier

from src.evaluation.metrics import alert_metrics, classification_metrics, merge_metrics
from src.evaluation.plots import plot_series
from src.quantum.feature_maps import circuit_metrics, get_feature_map


def run_vqc(X_train, X_test, y_train, y_test, n_qubits: int, maxiter: int, output_dir: str, threshold: float, seed: int) -> dict:
    feature_map = get_feature_map(n_qubits=n_qubits, map_type="zz")
    ansatz = RealAmplitudes(num_qubits=n_qubits, reps=2)
    qml = circuit_metrics(feature_map.compose(ansatz))
    losses = []
    start = time.perf_counter()

    try:
        from qiskit_algorithms.optimizers import COBYLA
        from qiskit_machine_learning.algorithms import VQC

        def callback(_, value):
            losses.append(float(value))

        model = VQC(feature_map=feature_map, ansatz=ansatz, optimizer=COBYLA(maxiter=maxiter), callback=callback)
        logging.getLogger("qiskit_machine_learning").setLevel(logging.ERROR)
        logging.getLogger().setLevel(logging.ERROR)
        model.fit(X_train, y_train)
        fit_result = getattr(model, "fit_result", None)
        if fit_result is not None:
            losses.append(float(fit_result.fun))
        training_time = time.perf_counter() - start
        start = time.perf_counter()
        pred = model.predict(X_test).astype(int)
        score = pred
        inference_time = time.perf_counter() - start
        mode = "qiskit"
    except Exception:
        model = MLPClassifier(hidden_layer_sizes=(8,), max_iter=1, warm_start=True, random_state=seed)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            for _ in range(maxiter):
                model.fit(X_train, y_train)
                losses.append(float(model.loss_))
        training_time = time.perf_counter() - start
        start = time.perf_counter()
        pred = model.predict(X_test)
        score = model.predict_proba(X_test)[:, 1]
        inference_time = time.perf_counter() - start
        mode = "classical_variational_fallback"

    plot_series(losses, output_dir, "vqc_convergence.png", "Convergência VQC", "loss")
    qml.update(
        {
            "training_time_seconds": training_time,
            "inference_time_seconds": inference_time,
            "optimizer_iterations": len(losses) if mode != "qiskit" else int(getattr(getattr(model, "fit_result", None), "nfev", maxiter) or maxiter),
            "final_loss": float(losses[-1]) if losses else np.nan,
            "vqc_backend": mode,
        }
    )
    return merge_metrics("VQC", classification_metrics(y_test, pred, score), alert_metrics(y_test, score, threshold), qml)
