import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Estimator

def build_hamiltonian(n_qubits=4):
    # Hamiltoniano DDoS simplificado: soma de Z_i
    terms = [("Z" + "I" * (n_qubits - i - 1), 1.0) for i in range(n_qubits)]
    return SparsePauliOp.from_list(terms)

def compute_anomaly_score(circuit, n_qubits=4):
    hamiltonian = build_hamiltonian(n_qubits)
    estimator   = Estimator()
    job         = estimator.run([circuit], [hamiltonian])
    return job.result().values[0]