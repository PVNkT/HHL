import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from QPE import QPE, qpe_qiskit
from rotation import rotation, Reciprocal

def circuit(A, nl, delta, wrap = True):
    nf = 1
    t = 2* np.pi * delta
    neg_vals = True
    qc_qpe, nb = QPE(nl, A, t)
    qc_qpet = QPE(nl, A, t, adjoint = False)[0].inverse()
    #qc_qpe, nb = qpe_qiskit(nl, A, t)
    #qc_qpet = qpe_qiskit(nl, A, t, adjoint = False)[0].inverse()
    nl_rg = QuantumRegister(nl, "state")
    nb_rg = QuantumRegister(nb, "q")
    #na_rg = QuantumRegister(nl, "a")
    nf_rg = QuantumRegister(nf, "flag")
    cf = ClassicalRegister(nf)
    cb = ClassicalRegister(nb)
    qc = QuantumCircuit(nb_rg, nl_rg,nf_rg, cf, cb)

    qc.h(nb_rg[0])
    
    qc.barrier()
    #qc_qpet = qc_qpe.inverse()
    #qc_rot = rotation(nl).reverse_bits()
    qc_rot = Reciprocal(nl, delta = delta*(2**(nl-1)), neg_vals = neg_vals)
    #qc = qc + qc_qpe + qc_rot + qc_qpet
    if wrap:
        qc.append(qc_qpe,nl_rg[:]+nb_rg[:])
        qc.append(qc_rot,[nl_rg[2]]+[nl_rg[1]]+[nl_rg[0]]+nf_rg[:])#.to_instruction(label="1/x")
        qc.append(qc_qpet,nl_rg[:]+nb_rg[:])
    else:
        qc = qc.compose(qc_qpe,nl_rg[:]+nb_rg[:])
        qc = qc.compose(qc_rot,[nl_rg[2]]+[nl_rg[1]]+[nl_rg[0]]+nf_rg[:])#.to_instruction(label="1/x")
        qc = qc.compose(qc_qpet,nl_rg[:]+nb_rg[:])
    qc.barrier()
    #qc.x(nb_rg[1])
    qc.measure(nf_rg,cf)
    qc.measure(nb_rg,cb)
    qc.draw("mpl").savefig("HHL_circuit.png")
    return qc