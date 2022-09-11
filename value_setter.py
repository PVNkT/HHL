import numpy as np

def get_eigenvalue(A):
    lambda_max = max(np.abs(np.linalg.eigvals(A)))
    lambda_min = min(np.abs(np.linalg.eigvals(A)))
    if np.any(np.linalg.eigvals(A)< 0):
        neg_vals = True
    else:
        neg_vals = False
    return lambda_max, lambda_min, neg_vals

def value_setter(A):
    lambda_max, lambda_min, neg_vals = get_eigenvalue(A)
    kappa = np.linalg.cond(A)
    nb = int(np.log2(len(A[0])))
    n_l = max(nb + 1, int(np.ceil(np.log2(kappa + 1)))) + neg_vals
    formatstr = "#0" + str(n_l-neg_vals + 2) + "b"
    lambda_min_tilde = np.abs(lambda_min * (2**(n_l-neg_vals) - 1) / lambda_max)
    # floating point precision can cause problems
    if np.abs(lambda_min_tilde - 1) < 1e-7:
        lambda_min_tilde = 1
    binstr = format(int(lambda_min_tilde), formatstr)[2::]
    lamb_min_rep = 0
    for i, char in enumerate(binstr):
        lamb_min_rep += int(char) / (2 ** (i + 1))
    delta = lamb_min_rep
    evolution_time = 2 * np.pi * delta / lambda_min / (2**neg_vals)
    return n_l, evolution_time, delta
