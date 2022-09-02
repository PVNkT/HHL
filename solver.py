import numpy as np
from circuit import circuit
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.quantum_info import Statevector
from normalize import normalize_vector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister


def HHL_my(A, delta, wrap = True):
    qc = circuit(A, 3, delta, wrap = wrap)
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 8192
    t_qpe = transpile(qc, aer_sim)
    qobj = assemble(t_qpe, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()
    vector = normalize_vector(answer)
    return vector
def HHL_qiskit(A,b):
    backend = Aer.get_backend('aer_simulator')
    hhl = HHL(quantum_instance=backend)
    solution = hhl.solve(A, b)
    solution.state.draw("mpl").savefig("HHL_circuit_qiskit.png")
    naive_sv = Statevector(solution.state).data
    naive_full_vector = np.array([naive_sv[64], naive_sv[65], naive_sv[66], naive_sv[67]])
    
    naive_full_vector = np.real(naive_full_vector)
    return naive_full_vector/np.linalg.norm(naive_full_vector)