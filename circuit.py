import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from QPE import QPE, qpe_qiskit
from rotation import rotation

def circuit(A, nl, t):
    nf = 1
    #qc_qpe, nb = QPE(nl, A, t)
    #qc_qpet = QPE(nl, A.T, t)[0].inverse()
    qc_qpe, nb = qpe_qiskit(nl, A, t)
    qc_qpet = qpe_qiskit(nl, A.T, t)[0].inverse()
    nl_rg = QuantumRegister(nl, "eval")
    nb_rg = QuantumRegister(nb, "q")
    na_rg = QuantumRegister(nl, "a")
    nf_rg = QuantumRegister(nf, "f")
    cf = ClassicalRegister(nf)
    cb = ClassicalRegister(nb)
    qc = QuantumCircuit(nb_rg, nl_rg,nf_rg, na_rg, cf, cb)

    qc.h(nb_rg[0])
    qc.barrier()
    #qc_qpet = qc_qpe.inverse()
    qc_rot = rotation(nl)
    qc = qc + qc_qpe + qc_rot + qc_qpet
    qc.barrier()
    qc.measure(nf_rg,cf)
    qc.measure(nb_rg,cb)
    print(qc)
    return qc