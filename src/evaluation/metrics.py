from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score


def classification_metrics(y_true, y_pred, y_score=None) -> dict:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    try:
        roc_auc = roc_auc_score(y_true, y_score if y_score is not None else y_pred)
    except ValueError:
        roc_auc = float("nan")
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc,
        "confusion_matrix": cm.tolist(),
        "false_positive_rate": fp / max(fp + tn, 1),
        "false_negative_rate": fn / max(fn + tp, 1),
    }


def alert_metrics(y_true, scores, threshold: float = 0.5) -> dict:
    scores = np.asarray(scores, dtype=float)
    alerts = np.where(scores >= threshold)[0]
    true_alerts = int(np.sum(np.asarray(y_true)[alerts] == 1)) if len(alerts) else 0
    false_alerts = int(len(alerts) - true_alerts)
    first_attack = np.where(np.asarray(y_true) == 1)[0]
    detected_attack = [idx for idx in alerts if y_true[idx] == 1]
    etd = float(detected_attack[0] - first_attack[0]) if len(first_attack) and detected_attack else float("nan")
    return {
        "number_of_alerts": int(len(alerts)),
        "true_alerts": true_alerts,
        "false_alerts": false_alerts,
        "alert_precision": true_alerts / max(len(alerts), 1),
        "estimated_time_to_detection": etd,
        "mitigation_delay_simulated": 2.0 + max(etd, 0.0) * 0.1 if not np.isnan(etd) else float("nan"),
    }


def merge_metrics(model: str, metrics: dict, alerts: dict, qml: dict | None = None) -> dict:
    row = {"model": model}
    row.update(metrics)
    row.update(alerts)
    row.update(qml or {})
    return row
