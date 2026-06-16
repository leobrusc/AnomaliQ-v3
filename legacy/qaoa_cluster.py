from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

def run_qaoa(qubit_op, reps=1):
    optimizer = COBYLA(maxiter=100)
    sampler   = Sampler()
    qaoa      = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    result    = qaoa.compute_minimum_eigenvalue(qubit_op)
    return result