import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.arithmetic.piecewise_chebyshev import PiecewiseChebyshev
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.circuit.library.arithmetic.exact_reciprocal import ExactReciprocal

def rotation(nl):
    c = 1 
    f_x, degree, breakpoints, num_state_qubits = lambda x: np.arcsin(c / x), 2, [1,2,3,4], nl
    pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
    pw_approximation._build()

    nl_rg = QuantumRegister(nl, "eval")
    na_rg = QuantumRegister(nl, "a")
    nf_rg = QuantumRegister(1, "f")
    qc = QuantumCircuit(nl_rg, nf_rg, na_rg)
    qc.append(pw_approximation,nl_rg[:]+[nf_rg[0]]+na_rg[:])
    return qc

def Reciprocal(nl, delta, neg_vals):
    reciprocal_circuit = ExactReciprocal(nl, delta, neg_vals=neg_vals)
    return reciprocal_circuit

if __name__ == "__main__":
    nl = 3
    c = 1 
    f_x, degree, breakpoints, num_state_qubits = lambda x: np.arcsin(c / x), 2, [1,2,3,4], nl
    pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
    print(pw_approximation.qubits) 
