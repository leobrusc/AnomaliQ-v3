from __future__ import annotations

import time

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from src.evaluation.metrics import alert_metrics, classification_metrics, merge_metrics


def _score(model, X):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    if hasattr(model, "decision_function"):
        scores = model.decision_function(X)
        return (scores - scores.min()) / max(scores.max() - scores.min(), 1e-9)
    return model.predict(X)


def run_classical_baselines(X_train, X_test, y_train, y_test, threshold: float, seed: int) -> list[dict]:
    models = {
        "SVM-RBF": SVC(kernel="rbf", probability=True, random_state=seed),
        "Random Forest": RandomForestClassifier(n_estimators=160, max_depth=8, random_state=seed, n_jobs=1),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=seed),
    }
    try:
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            n_estimators=120,
            max_depth=4,
            learning_rate=0.07,
            subsample=0.9,
            eval_metric="logloss",
            random_state=seed,
        )
    except Exception:
        pass

    rows = []
    for name, model in models.items():
        try:
            start = time.perf_counter()
            model.fit(X_train, y_train)
            training_time = time.perf_counter() - start
            start = time.perf_counter()
            y_pred = model.predict(X_test)
            y_score = _score(model, X_test)
            inference_time = time.perf_counter() - start
            rows.append(
                merge_metrics(
                    name,
                    classification_metrics(y_test, y_pred, y_score),
                    alert_metrics(y_test, y_score, threshold),
                    {"training_time_seconds": training_time, "inference_time_seconds": inference_time},
                )
            )
        except Exception:
            continue

    iso = IsolationForest(contamination=max(float(np.mean(y_train)), 0.01), random_state=seed)
    start = time.perf_counter()
    iso.fit(X_train[y_train == 0])
    training_time = time.perf_counter() - start
    start = time.perf_counter()
    raw = -iso.decision_function(X_test)
    score = (raw - raw.min()) / max(raw.max() - raw.min(), 1e-9)
    pred = (score >= np.percentile(score, 100 * (1 - np.mean(y_train)))).astype(int)
    inference_time = time.perf_counter() - start
    rows.append(
        merge_metrics(
            "Isolation Forest",
            classification_metrics(y_test, pred, score),
            alert_metrics(y_test, score, threshold),
            {"training_time_seconds": training_time, "inference_time_seconds": inference_time},
        )
    )
    return rows
