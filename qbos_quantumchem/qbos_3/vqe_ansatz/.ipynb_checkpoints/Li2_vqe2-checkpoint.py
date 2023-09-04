#!/usr/bin/env python3


import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np

enuc = 3.0*3.0/5.05 #nuclear repulsion of Li2 molecule, 5.05 a.u. apart

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 2 #number of qubits
    qv.ham = "-16.13589749302388 + -0.1905871485441244 Z1+ -0.1905871485441244 Z0+ 0.02951872455255705 X1+ 0.02951872455255705 X0+ -0.012244760076870108 Y0 Y1+ 0.01435069497554554 X0 Z1+ 0.01435069497554554 Z0 X1+ 0.022106056994702104 X0 X1+ 0.0961696471736273 Z0 Z1"
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
                
print("-------- Li2 (2 qubit) --------")
print("E_nuc = %.12f" % enuc)
print("E_SCF = %.12f" % (escf + enuc))
print("E_VQE = %.12f" % (evqe + enuc))
print("(E_corr = %.12f)" % (evqe - escf))
print("-------------------------------")


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
cisolver = ci.CISD(mf,  frozen = [0,1,3,6,7,8])
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
