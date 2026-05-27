from qiskit.circuit.library import ZZFeatureMap, PauliFeatureMap

def get_feature_map(n_qubits=4, reps=2, map_type="zz"):
    if map_type == "zz":
        return ZZFeatureMap(
            feature_dimension=n_qubits,
            reps=reps,
            entanglement="linear"
        )
    elif map_type == "pauli":
        return PauliFeatureMap(
            feature_dimension=n_qubits,
            reps=reps
        )
    else:
        raise ValueError(f"Feature map '{map_type}' não suportado.")