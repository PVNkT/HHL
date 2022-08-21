import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from QPE import QPE
from rotation import rotation
def circuit(CU, b, nl, nf = 1):
    nb = int(np.log2(b.shape))
    nl_rg = QuantumRegister(nl, "l")
    nb_rg = QuantumRegister(nb, "b")
    na_rg = QuantumRegister(nl, "a")
    nf_rg = QuantumRegister(nf, "f")
    cf = ClassicalRegister(nf)
    cb = ClassicalRegister(nb)
    qc = QuantumCircuit(nl_rg,nf_rg, na_rg, nb_rg, cf, cb)
    qc.h(nb_rg[1])
    qc_qpe = QPE(nl, b, CU)
    qc_qpet = qc_qpe.inverse()
    qc_rot = rotation(nl)
    qc = qc + qc_qpe + qc_rot + qc_qpet
    qc.measure(nf_rg,cf)
    qc.measure(nb_rg,cb)
    return qc