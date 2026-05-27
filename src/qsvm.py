from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC

def train_qsvm(feature_map, X_train, y_train):
    kernel = FidelityQuantumKernel(feature_map=feature_map)
    model  = QSVC(quantum_kernel=kernel)
    model.fit(X_train, y_train)
    return model

def predict_qsvm(model, X_test):
    return model.predict(X_test)