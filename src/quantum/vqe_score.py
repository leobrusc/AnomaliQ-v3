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


def run_vqe_score(X_train, X_test, y_train, y_test, n_qubits: int, threshold: float) -> dict:
    fmap = get_feature_map(n_qubits=n_qubits, map_type="zz")
    hamiltonian = build_ddos_hamiltonian(n_qubits)
    start = time.perf_counter()
    train_scores = np.asarray([Statevector.from_instruction(fmap.assign_parameters(x)).expectation_value(hamiltonian).real for x in X_train])
    cutoff = np.percentile(train_scores[y_train == 0], 90)
    training_time = time.perf_counter() - start
    start = time.perf_counter()
    raw = np.asarray([Statevector.from_instruction(fmap.assign_parameters(x)).expectation_value(hamiltonian).real for x in X_test])
    pred = (raw >= cutoff).astype(int)
    score = (raw - raw.min()) / max(raw.max() - raw.min(), 1e-9)
    inference_time = time.perf_counter() - start
    qml = circuit_metrics(fmap)
    qml.update({"training_time_seconds": training_time, "inference_time_seconds": inference_time})
    return merge_metrics("VQE Hamiltonian Score", classification_metrics(y_test, pred, score), alert_metrics(y_test, score, threshold), qml)
