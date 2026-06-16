import numpy as np

class FALQON:
    """Adaptação temporal simplificada inspirada no FALQON."""

    def __init__(self, learning_rate=0.01):
        self.lr     = learning_rate
        self.params = None

    def initialize(self, n_params):
        self.params = np.zeros(n_params)

    def update(self, gradient):
        if self.params is None:
            raise ValueError("Inicialize os parâmetros primeiro.")
        self.params -= self.lr * gradient
        return self.params