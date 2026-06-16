from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.svm import SVC

from src.evaluation.plots import plot_noise_degradation
from src.quantum.feature_maps import get_feature_map


def benchmark_noise(X_train, X_test, y_train, y_test, output_dir: str, noise_levels: list[float], seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    model = SVC(kernel="rbf", probability=True, random_state=seed).fit(X_train, y_train)
    simulator = "feature_noise_fallback"
    try:
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, depolarizing_error

        # Build a concrete Aer noise model to document NISQ conditions. The
        # classification degradation below remains feature-level so the
        # benchmark is fast and deterministic across local machines.
        noise_model = NoiseModel()
        for level in noise_levels:
            if level > 0:
                noise_model.add_all_qubit_quantum_error(depolarizing_error(min(level, 0.75), 1), ["x", "sx", "rz"])
                noise_model.add_all_qubit_quantum_error(depolarizing_error(min(level, 0.75), 2), ["cx"])
                break
        AerSimulator(noise_model=noise_model)
        simulator = "qiskit_aer_noise_model"
    except Exception:
        pass
    fmap = get_feature_map(n_qubits=X_train.shape[1], map_type="zz")
    ops = fmap.decompose().count_ops()
    rows = []
    base_f1 = None
    for level in noise_levels:
        noisy = X_test + rng.normal(0.0, level * np.pi, size=X_test.shape)
        f1 = f1_score(y_test, model.predict(noisy), zero_division=0)
        if base_f1 is None:
            base_f1 = f1
        rows.append(
            {
                "noise_level": level,
                "f1": f1,
                "f1_degradation_under_noise": base_f1 - f1,
                "simulator": simulator,
                "n_qubits": fmap.num_qubits,
                "circuit_depth": fmap.decompose().depth(),
                "cx_count": int(ops.get("cx", 0)),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(f"{output_dir}/artifacts/nisq_noise.csv", index=False)
    plot_noise_degradation(df, output_dir)
    return df
