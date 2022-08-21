import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library.arithmetic.piecewise_chebyshev import PiecewiseChebyshev
from qiskit import IBMQ, Aer, transpile, assemble

nl = 3
f_x, degree, breakpoints, num_state_qubits = lambda x: np.arcsin(1 / x), 2, [1,2,3,4], nl
pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
pw_approximation._build()

qc = QuantumCircuit(nl*2+1)
qc.h([0,1,2])
qc.append(pw_approximation,range(nl*2+1))
qc.measure_all()
print(qc)

aer_sim = Aer.get_backend('aer_simulator')
shots = 4096
t_qpe = transpile(qc, aer_sim)
qobj = assemble(t_qpe, shots=shots)
results = aer_sim.run(qobj).result()
answer = results.get_counts()

print(answer)
