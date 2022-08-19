import qiskit
from scipy.linalg import expm
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info.operators import Operator
from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control
from qiskit import IBMQ, Aer, transpile, assemble

A_origin = np.array([[2,-1],[1,4]])
A = np.vstack((np.hstack((np.zeros_like(A_origin),A_origin)),np.hstack((A_origin.T, np.zeros_like(A_origin)))))
A = np.matrix(A)
b = np.array([1,1])
i = complex(0,1)
t = np.pi*2/16
U = expm(i*A*t)
U = np.matrix(U)
n_b = int(np.log2(U.shape[0]))
U_gate = UnitaryGate(U)
CU = add_control(U_gate,1,ctrl_state=None, label="CU")


def qft_dagger(qc, n):
    """n-qubit QFTdagger the first n qubits in circ"""
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)

n_l = 3
nl_rg = QuantumRegister(n_l, "l")
nb_rg = QuantumRegister(n_b, "b")
classical_rg = ClassicalRegister(n_l)
qc = QuantumCircuit(nl_rg,nb_rg,classical_rg)
for l in range(n_l):
    qc.h(nl_rg[l])
    for power in range(2**(l)):
        qc.append(CU, [nl_rg[l],nb_rg[0],nb_rg[1]])
qc.barrier()
qft_dagger(qc, 3)
qc.barrier()
qc.measure(nl_rg,classical_rg)
print(qc)

aer_sim = Aer.get_backend('aer_simulator')
shots = 2048
t_qpe = transpile(qc, aer_sim)
qobj = assemble(t_qpe, shots=shots)
results = aer_sim.run(qobj).result()
answer = results.get_counts()

print(answer)