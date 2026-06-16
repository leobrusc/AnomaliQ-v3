from __future__ import annotations

import time

from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from sklearn.svm import SVC

from src.evaluation.metrics import alert_metrics, classification_metrics, merge_metrics
from src.quantum.feature_maps import circuit_metrics, get_feature_map


def run_qsvm(X_train, X_test, y_train, y_test, n_qubits: int, map_type: str, threshold: float, seed: int) -> dict:
    feature_map = get_feature_map(n_qubits=n_qubits, map_type=map_type)
    qml = circuit_metrics(feature_map)
    name = f"QSVM-{map_type.upper()}"
    try:
        model = QSVC(quantum_kernel=FidelityQuantumKernel(feature_map=feature_map))
    except Exception:
        model = SVC(kernel="rbf", probability=True, random_state=seed)
        name += " fallback"

    start = time.perf_counter()
    model.fit(X_train, y_train)
    training_time = time.perf_counter() - start
    start = time.perf_counter()
    pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        score = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        raw = model.decision_function(X_test)
        score = (raw - raw.min()) / max(raw.max() - raw.min(), 1e-9)
    else:
        score = pred
    inference_time = time.perf_counter() - start
    qml.update({"training_time_seconds": training_time, "inference_time_seconds": inference_time})
    return merge_metrics(name, classification_metrics(y_test, pred, score), alert_metrics(y_test, score, threshold), qml)
