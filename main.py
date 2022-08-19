import qiskit
from scipy.linalg import expm
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info.operators import Operator
from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control
A_origin = np.array([[2,-1],[1,4]])
A = np.vstack((np.hstack((np.zeros_like(A_origin),A_origin)),np.hstack((A_origin.T, np.zeros_like(A_origin)))))
A = np.matrix(A)
b = np.array([1,1])
i = complex(0,1)
t = np.pi*2/16
U = expm(i*A*t)
U = np.matrix(U)
U_gate = UnitaryGate(U)
CU = add_control(U_gate,1,ctrl_state=None, label="CU")
controls = QuantumRegister(3)
circuit = QuantumCircuit(controls)
circuit.append(CU, [0,1,2])
print(circuit)