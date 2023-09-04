#!/usr/bin/env python3

import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np
from pyscf import gto

#nuclear repulsion of h2o
mol = gto.Mole()
mol.build(
        atom = '''H  0.0 0.0 0.0;
H  0.0  0.0  1.4;
H  0.0  0.0  2.8''',
        unit = 'B',
        basis = 'sto-3g',
        symmetry = 'Dooh',
        spin = 1
        )
enuc = mol.energy_nuc()

# to handle the HEA default ansatz
n_qubits = 2
n_layers = n_qubits * 8
n_params = 3 * n_qubits * n_layers

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 2 #number of qubits
    qv.ham = "-1.8708513651737868 + -0.6858261906669804 Z1+ -0.6676677988223944 Z0+ -0.11477657448285694 X1+ 0.10944831520428308 X0+ -0.0706831956574033 Y0 Y1+ -0.06270219200063257 Z0 Z1+ -0.02789888490117795 X0 Z1+ -0.026471182130420462 Z0 X1+ 0.05791926293655267 X0 X1"
    qv.ansatz = "default"
    qv.ansatz_depth = n_layers
    qv.theta = qbos_op.ND()
    for i in range(n_params):
        qv.theta[0][0][i] = theta[i]
    qv.run()
    return qv.out_energy[0][0][0]

#(2) connect to optimizer and print results
escf = qbvqe(n_params*[0.0]) #get HF energy from initial guess
theta = np.array(n_params*[0.0])
res = minimize(qbvqe, 
               theta, 
               method = 'SLSQP', 
               options = {'maxiter' : 50, 'ftol' : 1e-12},
               bounds = Bounds(-np.pi, np.pi, True))
evqe = res.fun
print("-------------------------------")
if (res.nit < 50):
    print("VQE converged in " + str(res.nit) + " iterations!")
else:
    print("Beware! VQE might not have converged in " + str(res.nit) + " iterations!")
                
print("-------- H2O (2 qubit) --------")
print("E_nuc = %.12f" % enuc)
print("E_SCF = %.12f" % (escf + enuc))
print("E_VQE = %.12f" % (evqe + enuc))
print("(E_corr = %.12f)" % (evqe - escf))
print("-------------------------------")


#for comparison only!
print("----- Comparison to PySCF -----")

from pyscf import gto, scf, ci, fci

# (2) do SCF
mf = scf.RHF(mol)
mf.conv_tol = 1e-12
mf.conv_tol_grad = 1e-12
mf.max_cycle = 100
mf.kernel()
escf = mf.e_tot

# (3) do FCI
fcisolver = fci.FCI(mf)
fcisolver.conv_tol = 1e-12
efci = fcisolver.kernel()[0]

# (4) print results
print("---------------------------")
print("{:>11} | {:>16}".format('Method','Energy [a.u.]'))
print("---------------------------")
print("{0:<11} | {1:>16.12f}".format('SCF', escf))
print("{0:<11} | {1:>16.12f}".format('FCI (exact)', efci))
print("{0:<11} | {1:>16.12f}".format('VQE', evqe + enuc))



#OUTPUT:
#-------------------------------
#VQE converged in 14 iterations!
#-------- H2O (2 qubit) --------
#E_nuc = 1.785714285714
#E_SCF = -1.501333260950
#E_VQE = -1.526643084271
#(E_corr = -0.025309823321)
#-------------------------------
#----- Comparison to PySCF -----
#converged SCF energy = -1.50133326094951
#---------------------------
#     Method |    Energy [a.u.]
#---------------------------
#SCF         |  -1.501333260950
#FCI (exact) |  -1.526643084271
#VQE         |  -1.526643084271