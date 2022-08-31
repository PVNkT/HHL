import numpy as np
from circuit import circuit
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.quantum_info import Statevector
from normalize import normalize_vector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.algorithms.linear_solvers.numpy_linear_solver import NumPyLinearSolver

def main(A, delta):
    qc = circuit(A, 3, delta)
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

if __name__ == "__main__":
    A = np.array([[2,-1],[1,4]])
    #A = np.array([[0,2,0,-1],[2,0,1,0],[0,1,0,4],[-1,0,4,0]])
    A_hermition = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A)))))
    #A = np.array([[3,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,4]])
    b = np.array([1,1,0,0])
    #b = np.array([1,1,1,1])
    delta = 1/16
    print(main(A,delta))
    print(HHL_qiskit(A_hermition,b))
    classical_solution = NumPyLinearSolver().solve(A_hermition, b / np.linalg.norm(b))
    print('classical state:', classical_solution.state/np.linalg.norm(classical_solution.state))