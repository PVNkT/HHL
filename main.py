import numpy as np
from solver import HHL_my, HHL_qiskit
from qiskit.algorithms.linear_solvers.numpy_linear_solver import NumPyLinearSolver

"""
HHL 알고리즘에 대한 이해를 위해서 qiskit에서 제공하는 HHL 알고리즘의 코드를 기반으로 코드를 재구성해 보았다.
이 코드에서는 qiskit의 HHL 코드에서 몇개의 변수에 대한 계산을 생략하고 특정한 값을 넣어서 작동시켰다.
임의의 선형 방정식 Ax=b (A가 Hermition이 아니여도 됨)에 대해서 A와 b가 주어졌을 때 normalize된 x 벡터를 구하는 코드이다. 
실제 값을 얻기 위해서는 normalize된 벡터를 다시 Ax = b에 대입하여 특정한 상수를 구해주는 과정이 추가적으로 필요하다.
"""
def main(A, b, wrap = True):
    #A가 Hermition인지 아닌지를 확인하고 A가 Hermition이 아닐 경우 0벡터를 추가하여 Hermition의 형태가 되도록 한다.
    """
    ex) A = [[a,b],     
            [c,d]] 일때

    A = [[0,0,a,b],
        [0,0,c,d],
        [a*,c*,0,0],
        [b*,d*,0,0]] 의 형태로 바꾸어 Hermition으로 바꿍

    b = [e,
        f] 라면

    b = [e,
        f,
        0,
        0] 으로 바꾸어 원래의 식과 동일하게 바꾼다.
    """

    if np.allclose(A, A.conj().T):
        A = A
        b = b
    else:
        A = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.conj().T, np.zeros_like(A)))))
        b = np.hstack((b, np.zeros_like(b)))
    # delta를 통해서 evolution time t와 reciprocal 과정에서의 scaling을 결정한다. 이 코드에서는 임의의 값으로 설정함
    delta = 1/16
    #재구성한 모델
    my_sol = HHL_my(A, b, delta, wrap = wrap)
    #원본 qiskit 모델
    qiskit_sol = HHL_qiskit(A,b) 
    #고전적인 계산 결과
    classical_solution = NumPyLinearSolver().solve(A, b / np.linalg.norm(b))
    classical_sol = classical_solution.state/np.linalg.norm(classical_solution.state)

    print("my solution:", my_sol)
    print("qiskit solution:", qiskit_sol)
    print('classical solution:', classical_sol)
    #고전적인 결과와 비교하였을 때 모델에 대한 에러
    my_err = np.linalg.norm(classical_sol-my_sol)
    qiskit_err = np.linalg.norm(classical_sol-qiskit_sol)
    print("my error:", my_err)
    print("qiskit error:", qiskit_err)
if __name__ == "__main__":
    #A, b입력
    A = np.array([[2,-1],[1,4]])
    b = np.array([1,1])
    main(A,b)
    
    
