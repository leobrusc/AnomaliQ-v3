from __future__ import annotations

from qiskit.circuit.library import PauliFeatureMap, ZZFeatureMap


def get_feature_map(n_qubits: int = 4, reps: int = 2, map_type: str = "zz"):
    if map_type == "zz":
        return ZZFeatureMap(feature_dimension=n_qubits, reps=reps, entanglement="linear")
    if map_type == "pauli":
        return PauliFeatureMap(feature_dimension=n_qubits, reps=reps, paulis=["Z", "ZZ"])
    raise ValueError(f"Feature map não suportado: {map_type}")


def circuit_metrics(circuit) -> dict:
    ops = circuit.decompose().count_ops()
    return {
        "n_qubits": circuit.num_qubits,
        "circuit_depth": circuit.decompose().depth(),
        "num_parameters": len(circuit.parameters),
        "cx_count": int(ops.get("cx", 0)),
    }
