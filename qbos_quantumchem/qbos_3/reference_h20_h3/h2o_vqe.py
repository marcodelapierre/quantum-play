import qbos_op
from scipy.optimize import Bounds, minimize
import numpy as np
from pyscf import gto

#nuclear repulsion of h2o
mol = gto.Mole()
mol.build(
        atom = '''O  0.0 0.0 -0.73881674482711;
H  1.43103620092628  0.0  0.36940837241355;
H  -1.43103620092628  0.0  0.36940837241355''',
        unit = 'B',
        basis = 'sto-3g',
        symmetry = 'C2v'
        )
enuc = mol.energy_nuc()

# define vqe function for optimizer 
def qbvqe(theta):
    qv = qbos_op.vqe()
    qv.sn = 0 #non-stochastic run
    qv.qn = 2 #number of qubits
    qv.ham = "-83.25725311170568 + -0.571777174792345 Z0+ -0.1764363062038683 Z1+ 0.05765562087249579 X1+ 0.0753233343961892 X0+ -0.14683081784106378 Z0 Z1+ -0.05765562087250055 Z0 X1+ -0.006584794227654331 X0 Z1+ 0.01980854363989678 Y0 Y1+ 0.08878182442060809 X0 X1"
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

# (4) do frozen CISD to compare to VQE
cisolver = ci.CISD(mf,  frozen = [0,1,2,4])
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



#OUTPUT:
#-------------------------------
#VQE converged in 15 iterations!
#-------- H2O (2 qubit) --------
#E_nuc = 9.189273964612
#E_SCF = -74.963023445931
#E_VQE = -74.969102963979
#(E_corr = -0.006079518047)
#-------------------------------
#----- Comparison to PySCF -----
#converged SCF energy = -74.9630234459314
#E(RCISD) = -74.96910296397934  E_corr = -0.006079518047895641
#---------------------------
#     Method |    Energy [a.u.]
#---------------------------
#SCF         | -74.963023445931
#FCI (exact) | -75.012580021686
#frozen FCI  | -74.969102963979
#VQE         | -74.969102963979