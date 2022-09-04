import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.arithmetic.piecewise_chebyshev import PiecewiseChebyshev
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.circuit.library.arithmetic.exact_reciprocal import ExactReciprocal

#PiecewiseChebyshev를 사용해서 eigenvalue의 역수만큼 amplitude를 회전시키는 방법, 근사적인 방법을 사용해서 정확도가 떨어져서 결과가 잘 나오지 않는다.
def rotation(nl):
    #c는 A의 가장 작은 eigenvalue보다 작아야하지만 (확률은 최대 1이기 때문) 최대한 커야할 필요가 있다. (flag가 1로 측정될 확률을 늘리기 위해서)
    #c를 결정하는 방법이 존재 Haener, T., Roetteler, M., & Svore, K. M. (2018). Optimizing Quantum Circuits for Arithmetic. `arXiv:1805.12445 <http://arxiv.org/abs/1805.12445>`
    c = 1 
    #degree는 근사하는 polynomial의 최대 차수, breakpoint는 구간을 나누는 점들, num_state_qubits는 상태의 수. 이 값들 역시 최적값이 위의 논문에서 계산됨
    f_x, degree, breakpoints, num_state_qubits = lambda x: np.arcsin(c / x), 2, [1,2,3,4], nl
    #PiecewiseChebyshev를 사용한 회로를 만듬
    pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
    pw_approximation._build()

    #필요한 양자 register들을 만든다.
    nl_rg = QuantumRegister(nl, "eval")
    na_rg = QuantumRegister(nl, "a")
    nf_rg = QuantumRegister(1, "f")
    #양자 register들을 합쳐 양자 회로를 구성한다.
    qc = QuantumCircuit(nl_rg, nf_rg, na_rg)
    #양자 회로에 PiecewiseChebyshev를 적용해서 회로를 반환한다.
    qc.append(pw_approximation,nl_rg[:]+[nf_rg[0]]+na_rg[:])
    return qc

#qiskit에서 제공하는 ExactReciprocal함수를 사용해서 양자상태를 eignevalue의 역수만큼 정확하게 돌린다.
#arcsin을 통한 각도에 대한 계산을 고전 컴퓨터에서 시행하고 그 각도만큼 회전을 적용하기 때문에 정확하게 계산이 가능하다.
#delta는 scaling을 위한 값으로 들어가며 nl*scaling을 eigenvalue의 분자 부분으로 사용하게 된다. delta의 정확한 값은 eignevalue의 최소값을 사용해서 계산되어야 한다.
def Reciprocal(nl, delta, neg_vals):
    reciprocal_circuit = ExactReciprocal(nl, delta, neg_vals=neg_vals)
    return reciprocal_circuit


