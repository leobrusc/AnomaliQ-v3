from qiskit.circuit.library import RealAmplitudes
from qiskit_machine_learning.algorithms import VQC
from qiskit_algorithms.optimizers import COBYLA

def train_vqc(feature_map, X_train, y_train, n_qubits=4, maxiter=60):
    ansatz = RealAmplitudes(num_qubits=n_qubits, reps=2)
    model  = VQC(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=COBYLA(maxiter=maxiter)
    )
    model.fit(X_train, y_train)
    return model

def predict_vqc(model, X_test):
    return model.predict(X_test)