#!/usr/bin/env python3


import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np

enuc = 3.0*1.0/3.01 #nuclear repulsion of LiH molecule, 3.01 a.u. apart

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 2 #number of qubits
    ## this comes out of the run of `_prep.py` script
    qv.ham = "-8.27412462131459 + -0.27006470525930193 Z0+ -0.25203742835554155 Z1+ 0.009854759096095227 X1+ 0.017037474116480766 X0+ -0.07576596838820601 Y0 Y1+ -0.06254156794725252 Z0 Z1+ -0.009854759096094599 Z0 X1+ 0.006424616021402407 X0 Z1+ 0.04808296135884555 X0 X1"
    ## where does the ansatz come from?
    qv.ansatz ='''
.compiler xasm 
.circuit qbos_ansatz
.parameters theta
.qbit q
    Ry(q[0], theta[0]);
    Ry(q[1], theta[1]);
    CX(q[0], q[1]);
    Ry(q[1], theta[2]);
'''
    qv.theta = qbos_op.ND()
    qv.theta[0][0][0] = theta[0]
    qv.theta[0][0][1] = theta[1]
    qv.theta[0][0][2] = theta[2]
    qv.run()
    return qv.out_energy[0][0][0]

#(2) connect to optimizer and print results
escf = qbvqe([0.0, 0.0, 0.0]) #get HF energy from initial guess
theta = np.array([0.0, 0.0, 0.0])
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
                
print("-------- LiH (2 qubit) --------")
print("E_nuc = %.12f" % enuc)
print("E_SCF = %.12f" % (escf + enuc))
print("E_VQE = %.12f" % (evqe + enuc))
print("(E_corr = %.12f)" % (evqe - escf))
print("-------------------------------")


from pyscf import gto, scf, ci, fci

# (1) define molecule
mol = gto.Mole()
mol.build(
        atom = '''Li 0 0 -1.505; H 0 0 +1.505''',
        unit = 'B',
        basis = 'sto-3g',
        symmetry = 'Coov'
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
cisolver = ci.CISD(mf,  frozen = [0,2,3])
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
