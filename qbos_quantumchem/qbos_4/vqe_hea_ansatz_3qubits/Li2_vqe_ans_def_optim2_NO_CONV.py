#!/usr/bin/env python3


import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np

enuc = 3.0*3.0/5.05 #nuclear repulsion of Li2 molecule, 5.05 a.u. apart

# to handle the HEA default ansatz
n_qubits = 2
n_layers = n_qubits
n_params = 3 * n_qubits * n_layers

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 2 #number of qubits
    qv.ham = "-16.27681679833032 + -0.049667843237683584 Z1+ -0.04474965813281173 Z0+ 0.025554079092073276 X1+ 0.031918165121209256 X0+ -0.049667843237683584 Z0 Z1+ -0.011951254406893305 Y0 Y1+ 0.011951254406893303 X0 Z1+ 0.01569278217424128 Z0 X1+ 0.031918165121209256 X0 X1"
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
## where do the following values come from??
#theta = [2.740881, 0, 0, -0.035507, 0, 0, -0.33113, 0, 0, -0.200767, 0, 1.49012e-08]
res = minimize(qbvqe, 
               theta, 
               method = 'nelder-mead', 
               options = {'maxiter' : 50, 'ftol' : 1e-12}, 
               bounds = Bounds(-np.pi, np.pi, True))
evqe = res.fun
print("-------------------------------")
if (res.nit < 50):
    print("VQE converged in " + str(res.nit) + " iterations!")
else:
    print("Beware! VQE might not have converged in " + str(res.nit) + " iterations!")
                
print("-------- Li2 (2 qubit) --------")
print("E_nuc = %.12f" % enuc)
print("E_SCF = %.12f" % (escf + enuc))
print("E_VQE = %.12f" % (evqe + enuc))
print("(E_corr = %.12f)" % (evqe - escf))
print("-------------------------------")

print("PIPPO")
print(theta)

from pyscf import gto, scf, ci, fci

# (1) define molecule
mol = gto.Mole()
mol.build(
        atom = '''Li 0 0 -2.525; Li 0 0 +2.525''',
        unit = 'B',
        basis = 'sto-3g',
        symmetry = 'Dooh'
        )

# (2) do SCF
mf = scf.RHF(mol)
mf.conv_tol = 1e-12
mf.conv_tol_grad = 1e-12
mf.max_cycle = 200
mf.kernel()
escf = mf.e_tot

# (3) do FCI
fcisolver = fci.FCI(mf)
fcisolver.conv_tol = 1e-12
efci = fcisolver.kernel()[0]

# (4) do frozen CISD to compare to VQE
cisolver = ci.CISD(mf,  frozen = [0,1,6,7,8,9])
cisolver.conv_tol = 1e-12
eci = cisolver.kernel()[0] + mf.e_tot

# (4) print results
print("---------------------------")
print("{:>11} | {:>16}".format('Method','Energy [a.u.]'))
print("---------------------------")
print("{0:<11} | {1:>16.12f}".format('SCF', escf))
print("{0:<11} | {1:>16.12f}".format('FCI (exact)', efci))
print("{0:<11} | {1:>16.12f}".format('frozen FCI', eci))
print("{0:<11} | {1:>16.12f}".format('VQE', evqe + enuc))
