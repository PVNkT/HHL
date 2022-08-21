import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.arithmetic.piecewise_chebyshev import PiecewiseChebyshev
from qiskit import IBMQ, Aer, transpile, assemble

def rotation(nl):

    f_x, degree, breakpoints, num_state_qubits = lambda x: np.arcsin(1 / x), 2, [1,2,3,4], nl
    pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
    pw_approximation._build()
    nl_rg = QuantumRegister(nl, "l")
    na_rg = QuantumRegister(nl, "a")
    nf_rg = QuantumRegister(1, "f")
    qc = QuantumCircuit(nl_rg, na_rg, nf_rg)
    qc.h(nl_rg[:])
    qc.append(pw_approximation,range(nl*2+1))

    return qc
