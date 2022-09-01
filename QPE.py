import qiskit
from scipy.linalg import expm
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info.operators import Operator
from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control
from qiskit import IBMQ, Aer, transpile, assemble

from qiskit.circuit.library import PhaseEstimation
from unitary import Unitary, CUnitary

def qft(n, inverse = False):
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    #QFT의 역연산은 곧 QFT_dagger임을 기억하자.
    """
    #Swap gate 걸어주기 (qiskit에서는 큐빗을 반대로 읽기 때문.)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    """
    for j in reversed(range(n)):
        qc.h(j)
        for m in reversed(range(j)):
            qc.cp(np.pi * (2.0 ** (m - j)), m, j)
    if inverse:
        qc.inverse()
                
    qc.name = "QFT†"
    #display(qc.draw(output = 'mpl'))
    return qc

def QPE(n_l,A,t, adjoint = False):
    #circuit initialization for HHL
    CU, n_b = CUnitary(A, t, adjoint=adjoint)
    nl_rg = QuantumRegister(n_l, "state")
    nb_rg = QuantumRegister(n_b, "q")

    #QuantumRegister(size=None, name=None, bits=None) 
    qc = QuantumCircuit(nl_rg,nb_rg)
    qc.name = "QPE"
    #display(qc.draw(output = 'mpl'))
    qc.h(nl_rg[:]) #n_1 register에 하다마드 게이트를 모두 걸어줌
    qc.barrier()
    for l in range(n_l):
        for power in range(2**(l)):
            qc.append(CU, [nl_rg[l],nb_rg[0],nb_rg[1]]) 
            #첫번째 큐비트는 2^0번, 이후 2^n꼴로 돌아가게 설계됨.
            #https://qiskit.org/documentation/stubs/qiskit.circuit.ControlledGate.html append의 예제.
            #즉, append의 첫번째 인자는 gate, 두번쨰 인자의 첫번째 요소는 control qubit, 이후 인자의 요소는 target qubit.
    qc.barrier()
    qc.append(qft(n_l, inverse = True), range(n_l)) 
        #append안에 들어간 qft_dagger라는 함수가 반환하는 qc라는 회로에 이름을 지정하면 간단히 이름으로 표기 가능
    qc.barrier()
    #qc.measure(nl_rg,classical_rg)
    #display(qc.draw(output = 'mpl'))
    # qc2 = qc.inverse()
    # display(qc2.draw(output = 'mpl'))
    return qc, n_b

def qpe_qiskit(nl, A, t, adjoint=False):
    U, n_b = Unitary(A, t, adjoint=adjoint)
    qpe = PhaseEstimation(nl, U)
    return qpe, n_b
