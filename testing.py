from dtensor import dtensor
from ktensor import ktensor
from cp import als
import numpy as np

# 1.792620159
U = [np.random.rand(i,3) for i in (20, 10, 14)]
T = dtensor(ktensor(U).toarray())
P, fit, itr, _ = als(T, 3)
np.allclose(T, P.totensor())