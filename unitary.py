from xmlrpc.client import Boolean
import numpy as np
from scipy.linalg import expm
from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control

def CUnitary(A, t):
    A = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A)))))
    i = complex(0,1)
    U = expm(i*A*t)

    n_b = int(np.log2(U.shape[0]))
    U_gate = UnitaryGate(U)
    CU = add_control(U_gate,1,ctrl_state=None, label="CU")

    return CU, n_b

def Unitary(A, t):
    A = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A)))))
    #A = np.array([[0,2,0,-1],[2,0,1,0],[0,1,0,4],[-1,0,4,0]])
    i = complex(0,1)
    U = expm(i*A*t)
    U_gate = UnitaryGate(U)
    n_b = int(np.log2(U.shape[0]))
    return U_gate, n_b