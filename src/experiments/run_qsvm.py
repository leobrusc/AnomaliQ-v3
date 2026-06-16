from __future__ import annotations

import time
from sklearn.svm import SVC

from src.evaluation.metrics import alert_metrics, classification_metrics, merge_metrics
from src.evaluation.reports import append_rows
from src.experiments.common import finish, load_config, output_dir, parse_args, prepared_quantum, reset_outputs
from src.quantum.qsvm import run_qsvm


def run(config: dict):
    X_train, y_train, X_test, y_test, warnings = prepared_quantum(config)
    exp = config.get("experiments", {})
    threshold = float(exp.get("alert_threshold", 0.5))
    seed = int(config.get("seed", 42))
    n_qubits = int(config.get("preprocessing", {}).get("n_qubits", 4))
    rows = []
    start = time.perf_counter()
    svm = SVC(kernel="rbf", probability=True, random_state=seed).fit(X_train, y_train)
    training = time.perf_counter() - start
    start = time.perf_counter()
    pred = svm.predict(X_test)
    score = svm.predict_proba(X_test)[:, 1]
    rows.append(merge_metrics("SVM-RBF PCA baseline", classification_metrics(y_test, pred, score), alert_metrics(y_test, score, threshold), {"training_time_seconds": training, "inference_time_seconds": time.perf_counter() - start, "n_qubits": n_qubits}))
    for map_type in exp.get("qsvm_feature_maps", ["zz", "pauli"]):
        rows.append(run_qsvm(X_train, X_test, y_train, y_test, n_qubits, map_type, threshold, seed))
    return rows, warnings


def main():
    args = parse_args()
    config = load_config(args.config)
    out = output_dir(config)
    if args.reset:
        reset_outputs(out)
    rows, warnings = run(config)
    append_rows(out, rows)
    finish(out, warnings)


if __name__ == "__main__":
    main()
