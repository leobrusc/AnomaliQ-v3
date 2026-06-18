from __future__ import annotations

import time

import numpy as np
from qiskit.quantum_info import SparsePauliOp, Statevector

from src.evaluation.metrics import alert_metrics, classification_metrics, merge_metrics
from src.quantum.feature_maps import circuit_metrics, get_feature_map


def build_ddos_hamiltonian(n_qubits: int):
    terms = []
    for i in range(n_qubits):
        pauli = ["I"] * n_qubits
        pauli[n_qubits - i - 1] = "Z"
        terms.append(("".join(pauli), 1.0))
    for i in range(n_qubits - 1):
        pauli = ["I"] * n_qubits
        pauli[n_qubits - i - 1] = "Z"
        pauli[n_qubits - i - 2] = "Z"
        terms.append(("".join(pauli), 0.35))
    return SparsePauliOp.from_list(terms)


def _threshold_by_validation(scores: np.ndarray, labels: np.ndarray) -> tuple[float, str]:
    from sklearn.metrics import f1_score

    candidates = np.unique(np.percentile(scores, np.linspace(5, 95, 19)))
    best = (candidates[0], "high", -1.0)
    for cutoff in candidates:
        for direction in ["high", "low"]:
            pred = (scores >= cutoff).astype(int) if direction == "high" else (scores <= cutoff).astype(int)
            f1 = f1_score(labels, pred, zero_division=0)
            if f1 > best[2]:
                best = (float(cutoff), direction, float(f1))
    return best[0], best[1]


def _threshold_by_percentile(scores: np.ndarray, labels: np.ndarray, percentile: float) -> tuple[float, str]:
    benign = scores[labels == 0]
    high_cutoff = float(np.percentile(benign, percentile))
    low_cutoff = float(np.percentile(benign, 100 - percentile))
    attack = scores[labels == 1]
    high_separation = abs(float(np.mean(attack)) - high_cutoff) if len(attack) else 0.0
    low_separation = abs(float(np.mean(attack)) - low_cutoff) if len(attack) else 0.0
    return (high_cutoff, "high") if high_separation >= low_separation else (low_cutoff, "low")


def run_vqe_score(
    X_train,
    X_test,
    y_train,
    y_test,
    n_qubits: int,
    threshold: float,
    threshold_strategy: str = "validation",
    threshold_percentile: float = 90.0,
) -> dict:
    fmap = get_feature_map(n_qubits=n_qubits, map_type="zz")
    hamiltonian = build_ddos_hamiltonian(n_qubits)
    start = time.perf_counter()
    train_scores = np.asarray([Statevector.from_instruction(fmap.assign_parameters(x)).expectation_value(hamiltonian).real for x in X_train])
    if threshold_strategy == "validation":
        cutoff, direction = _threshold_by_validation(train_scores, y_train)
    else:
        cutoff, direction = _threshold_by_percentile(train_scores, y_train, threshold_percentile)
    training_time = time.perf_counter() - start
    start = time.perf_counter()
    raw = np.asarray([Statevector.from_instruction(fmap.assign_parameters(x)).expectation_value(hamiltonian).real for x in X_test])
    pred = (raw >= cutoff).astype(int) if direction == "high" else (raw <= cutoff).astype(int)
    score = (raw - raw.min()) / max(raw.max() - raw.min(), 1e-9)
    if direction == "low":
        score = 1.0 - score
    inference_time = time.perf_counter() - start
    qml = circuit_metrics(fmap)
    qml.update(
        {
            "training_time_seconds": training_time,
            "inference_time_seconds": inference_time,
            "vqe_threshold": cutoff,
            "vqe_threshold_strategy": threshold_strategy,
            "vqe_threshold_direction": direction,
            "vqe_score_note": "VQE Hamiltonian Score is continuous; classification metrics use configured thresholding.",
        }
    )
    return merge_metrics("VQE Hamiltonian Score", classification_metrics(y_test, pred, score), alert_metrics(y_test, score, threshold), qml)
