import numpy as np
from solver import HHL_my, HHL_qiskit
from qiskit.algorithms.linear_solvers.numpy_linear_solver import NumPyLinearSolver

def main(A, b, wrap = True):
    if np.allclose(A, A.conj().T):
        A = A
    else:
        A = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A)))))
    
    delta = 1/16
    my_sol = HHL_my(A,delta, wrap =wrap)
    qiskit_sol = HHL_qiskit(A,b) 
    classical_solution = NumPyLinearSolver().solve(A, b / np.linalg.norm(b))
    classical_sol = classical_solution.state/np.linalg.norm(classical_solution.state)
    print("my solution:", my_sol)
    print("qiskit solution:", qiskit_sol)
    print('classical solution:', classical_sol)
    my_err = np.linalg.norm(classical_sol-my_sol)
    qiskit_err = np.linalg.norm(classical_sol-qiskit_sol)
    print("my error:", my_err)
    print("qiskit error:", qiskit_err)
if __name__ == "__main__":
    A = np.array([[2,-1],[1,4]])
    b = np.array([1,1,0,0])
    main(A,b)
    
    
