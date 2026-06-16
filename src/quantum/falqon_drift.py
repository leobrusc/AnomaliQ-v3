from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.svm import SVC

from src.evaluation.plots import plot_series


def run_falqon_drift(X_train, X_test, y_train, y_test, output_dir: str, windows: int = 6, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    model = SVC(kernel="rbf", probability=True, random_state=seed).fit(X_train, y_train)
    f1_values = []
    chunks = np.array_split(np.arange(len(y_test)), windows)
    for i, idx in enumerate(chunks):
        drift = i / max(windows - 1, 1)
        Xw = X_test[idx].copy()
        Xw[y_test[idx] == 1] += rng.normal(drift * 0.35, 0.03, size=Xw[y_test[idx] == 1].shape)
        pred = model.predict(Xw)
        current_f1 = f1_score(y_test[idx], pred, zero_division=0)
        f1_values.append(float(current_f1))
        if i == windows // 2:
            model.fit(np.vstack([X_train, Xw]), np.concatenate([y_train, y_test[idx]]))
    plot_series(f1_values, output_dir, "falqon_drift.png", "FALQON POC - drift temporal", "F1")
    pd.DataFrame({"window": range(len(f1_values)), "f1": f1_values}).to_csv(f"{output_dir}/artifacts/falqon_drift.csv", index=False)
    return {
        "model": "FALQON Drift POC",
        "f1": float(np.mean(f1_values)),
        "min_window_f1": float(np.min(f1_values)),
        "recovered_f1": float(f1_values[-1]),
        "falqon_status": "Placeholder funcional: adaptação por retreino incremental; TODO implementar controle FALQON completo.",
    }
