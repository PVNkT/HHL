import numpy as np
from circuit import circuit
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.algorithms.linear_solvers.hhl import HHL
from qiskit.quantum_info import Statevector
from normalize import normalize_vector
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister


def HHL_my(A, b, delta, wrap = True):
    #기초 회로 구성, 입력값: A(행렬), b(벡터), nl(사용하는 qubit의 수, 높을 수록 정확도가 높아짐), delta(evolution time t와 reciprocal 과정에서의 scaling을 결정), wrap(회로를 합쳐서 볼지 결정)
    qc = circuit(A, b, 3, delta, wrap = wrap)
    #양자 회로를 시뮬레이션하는 코드
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 8192
    t_qpe = transpile(qc, aer_sim)
    qobj = assemble(t_qpe, shots=shots)
    results = aer_sim.run(qobj).result()
    #시뮬레이션된 결과를 dictionary로 받음
    answer = results.get_counts()
    #실험 결과를 통해서 noramlize된 결과를 얻음
    vector = normalize_vector(answer)
    return vector


def HHL_qiskit(A,b):
    #backend 설정
    backend = Aer.get_backend('aer_simulator')
    #qiskit HHL 코드를 불러옴
    hhl = HHL(quantum_instance=backend)
    #A, b에 대해서 HHL 회로를 구성
    solution = hhl.solve(A, b)
    #만들어진 회로를 그림으로 저장
    solution.state.draw("mpl").savefig("HHL_circuit_qiskit.png")
    #연산된 상태를 상태 벡터의 형태로 결과를 얻음
    naive_sv = Statevector(solution.state).data
    #상태 벡터에서 필요한 상태만을 골라서 저장함
    naive_full_vector = np.array([naive_sv[64], naive_sv[65], naive_sv[66], naive_sv[67]])
    #실수 부분만 취함
    naive_full_vector = np.real(naive_full_vector)
    #얻어진 벡터를 normalize하여 반환
    return naive_full_vector/np.linalg.norm(naive_full_vector)