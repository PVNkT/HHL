import numpy as np
from scipy.linalg import expm
from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control
from unitary import Unitary
from circuit import circuit
from qiskit import IBMQ, Aer, transpile, assemble

def main(A, b, t):
    CU, b = Unitary(A,b,t)
    qc = circuit(CU, b, 3)
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 2048
    t_qpe = transpile(qc, aer_sim)
    qobj = assemble(t_qpe, shots=shots)
    results = aer_sim.run(qobj).result()
    answer = results.get_counts()
    return answer
if __name__ == "__main__":
    A = np.array([[2,-1],[1,4]])
    b = np.array([1,1])
    t = np.pi*2/8
    print(main(A,b,t))