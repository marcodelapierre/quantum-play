#!/usr/bin/env python3


import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np

enuc = 3.0*3.0/5.05 #nuclear repulsion of Li2 molecule, 5.05 a.u. apart

# to handle the HEA default ansatz
n_qubits = 3
n_layers = n_qubits
n_params = 3 * n_qubits * n_layers

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 3 #number of qubits
    qv.ham = "-14.100794366937885 + -2.0651977583719585 Z2+ -0.7723070264845457 Z0+ -0.726691624072787 Z1+ 0.005285278754346796 X2+ 0.008385363099702501 X0+ 0.011076251087091342 X1+ -0.726691624072787 Z0 Z1+ -0.002700118229005769 Y0 Y1+ 0.0026480139295720043 X1 X2+ 0.0026480139295721526 Y1 Y2+ 0.002700118229005769 X0 Z1+ 0.005929239255359332 Z0 X1+ 0.008385363099702501 X0 Z2+ 0.008385363099702501 X0 X1+ 0.012275950632784532 X1 Z2+ 0.012620814602749374 Z0 X2+ 0.012981663085503196 Z1 X2+ 0.019213090504623137 X0 X2+ 0.019213090504623137 Y0 Y2+ 0.6423827362095622 Z0 Z2+ 0.6641987603959496 Z1 Z2+ -0.002700118229005769 Y0 Y1 Z2+ -0.001945666510916975 Y0 Y1 X2+ 0.001945666510916975 X0 X1 X2+ 0.001945666510916975 X0 Y1 Y2+ 0.001945666510916975 Y0 X1 Y2+ 0.0026480139295720043 Z0 X1 X2+ 0.0026480139295721526 Z0 Y1 Y2+ 0.002700118229005769 X0 Z1 Z2+ 0.0071289388010525225 Z0 X1 Z2+ 0.008385363099702501 X0 X1 Z2+ 0.012981663085503196 Z0 Z1 X2+ 0.019213090504623137 X0 Z1 X2+ 0.019213090504623137 Y0 Z1 Y2+ 0.6641987603959496 Z0 Z1 Z2"
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
theta = [2.318549,0.191968,0.447648,1.22194,-0.0507721,0.395064,0.160091,0.252349,0.729706,0.689498,0.153772,-0.135701,0.900598,1.37073,0.162499,1.16133,1.12142,0.0718026,-0.0336113,0.828039,0.164589,1.24475,0.199907,0.446597,0.00557747,1.83249,0.2662]
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
