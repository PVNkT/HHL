from xmlrpc.client import Boolean
import numpy as np
from scipy.linalg import expm
from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control

def Unitary(A, b, t, adjoint=False):
    if A == A.T:
        b = b.T
    else:
        A = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A)))))
        b = np.hstack((b,np.zeros_like(b))).T
    i = complex(0,1)
    if adjoint:
        U = expm(-i*A*t)
    else:
        U = expm(i*A*t)
    n_b = int(np.log2(U.shape[0]))
    U_gate = UnitaryGate(U)
    CU = add_control(U_gate,1,ctrl_state=None, label="CU")

    return CU, b