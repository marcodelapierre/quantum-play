#!/usr/bin/env python3


import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np

enuc = 1.0/1.4 #nuclear repulsion of H2 molecule, 1.4 a.u. apart

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 1 #number of qubits
    qv.ham = "-1.0423546457082926 + -0.7886453936399724 Z0+ 0.18125791479310838 X0"
    qv.ansatz = '''
.compiler xasm 
.circuit qbos_ansatz 
.parameters theta 
.qbit q 
    Ry(q[0], theta);
'''
    qv.theta = qbos_op.ND()
    qv.theta[0][0][0] = theta
    qv.run()
    return qv.out_energy[0][0][0]

#(2) connect to optimizer and print results
escf = qbvqe(0.0) #get HF energy from initial guess
theta = np.array([0.0])
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
                
print("-------- H2 (1 qubit) ---------")
print("E_nuc = %.12f" % enuc)
print("E_SCF = %.12f" % (escf + enuc))
print("E_VQE = %.12f" % (evqe + enuc))
print("(E_corr = %.12f)" % (evqe - escf))
print("-------------------------------")


from pyscf import gto, scf, ci

# (1) define molecule
mol = gto.Mole()
mol.build(
        atom = '''H 0 0 -0.7; H 0 0 +0.7''',
        unit = 'B',
        basis = 'sto-3g',
        symmetry = 'Dooh',
        )

# (2) do SCF
mf = scf.RHF(mol)
mf.conv_tol = 1e-12
mf.max_cycle = 200
mf.kernel()

# (3) do FCI
cisolver = ci.CISD(mf)
cisolver.conv_tol = 1e-12
efci = cisolver.kernel()[0] + mf.e_tot

# (4) print results
print("---------------------------")
print("{:>6} | {:>16}".format('Method','Energy [a.u.]'))
print("---------------------------")
print("{0:<6} | {1:>16.12f}".format('SCF', escf + enuc))
print("{0:<6} | {1:>16.12f}".format('FCI', efci))
print("{0:<6} | {1:>16.12f}".format('VQE', evqe + enuc))
