#!/usr/bin/env python3


import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np

enuc = 3.0*3.0/5.05 #nuclear repulsion of Li2 molecule, 5.05 a.u. apart

n_qubits = 3
n_layers = n_qubits
n_params = 3 * n_qubits * n_layers

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 3 #number of qubits
    qv.ham = "-16.14754771472385 + -0.12926908360647182 Z0+ -0.12578132573695022 Z1+ -0.049521709815583126 Z2+ -0.0013123576263730594 X0+ 0.002265909579812349 X2+ 0.008012239813377987 X1+ -0.019016529074990705 X1 Z2+ -0.01589255720631494 X0 Z1+ -0.010738713911531323 Y1 Y2+ -0.008646588328449036 Y0 Y1+ -0.0007586212476769407 Z1 X2+ -0.00014613342210045843 Z0 Z2+ 0.015155227132708296 X0 X1+ 0.018499351167425217 Y0 Y2+ 0.023288169512260974 Z0 X2+ 0.023905925307831262 Z0 X1+ 0.026083365955932004 X0 X2+ 0.02651373230595307 X0 Z2+ 0.02693433469155826 Z1 Z2+ 0.03362678259737922 X1 X2+ 0.08103166760413849 Z0 Z1+ -0.07660217792924184 Z0 Z1 Z2+ -0.020813565042076508 X0 Y1 Y2+ -0.016730148128047455 Y0 X1 Y2+ -0.0017086174761699706 Z0 X1 X2+ -0.001212540495361996 Z0 Y1 Y2+ -0.0010764673128300173 Y0 Y1 Z2+ 0.0016578713528537523 X0 X1 X2+ 0.004850767451405509 Y0 Y1 X2+ 0.0051598842268590715 X0 X1 Z2+ 0.011503166375990128 X0 Z1 X2+ 0.016451403421918268 Z0 Z1 X2+ 0.019087181164494864 Y0 Z1 Y2+ 0.027101562303022717 X0 Z1 Z2+ 0.030967783481884024 Z0 X1 Z2"
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
#theta = [2.318549,0.191968,0.447648,1.22194,-0.0507721,0.395064,0.160091,0.252349,0.729706,0.689498,0.153772,-0.135701,0.900598,1.37073,0.162499,1.16133,1.12142,0.0718026,-0.0336113,0.828039,0.164589,1.24475,0.199907,0.446597,0.00557747,1.83249,0.2662]
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
cisolver = ci.CISD(mf,  frozen = [0,1,7,8])
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

#OUTPUT
#---------------------------
#     Method |    Energy [a.u.]
#---------------------------
#SCF         | -14.638723925117
#FCI (exact) | -14.667341040173
#frozen FCI  | -14.666524679541
#VQE         | -14.666524679505