import numpy as np
from circuit import circuit
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.quantum_info import Statevector
from normalize import normalize_vector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def main(A, t):
    qc = circuit(A, 3, t)
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 8192
    t_qpe = transpile(qc, aer_sim)
    qobj = assemble(t_qpe, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()
    vector = normalize_vector(answer)
    return vector
def HHL_qiskit(A,b):
    naive_hhl_solution = HHL().solve(A, b)
    q4 = QuantumRegister(2, "q856")
    q5 = QuantumRegister(4, "q857")
    q6 = QuantumRegister(1, "q858")
    cl = ClassicalRegister(3)
    qc = QuantumCircuit(q4,q5,q6,cl)
    qc = qc + naive_hhl_solution.state
    qc.measure([6,0,1],[2,0,1])
    print(qc)
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 8192
    t_qpe = transpile(qc, aer_sim)
    qobj = assemble(t_qpe, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()
    vector = normalize_vector(answer)
    return vector

if __name__ == "__main__":
    A = np.array([[2,1],[-1,4]])
    #A = np.array([[0,2,0,-1],[2,0,1,0],[0,1,0,4],[-1,0,4,0]])
    A_hermition = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A)))))
    #A = np.array([[3,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,4]])
    b = np.array([1,1,0,0])
    #b = np.array([1,1,1,1])
    t = np.pi*2/16
    print(main(A,t))
    print(HHL_qiskit(A_hermition,b))