#!/usr/bin/env python3
import qb.core.optimization.vqee as qbOptVqe
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

#(1) Define wrapper function accepting a parameter list theta and returning the VQE energy (single iteration)
def qbvqe(theta):
    params = qbOptVqe.Params()
    params.acceleratorName = "qpp"
    params.nShots = 1024   # Number of shots
    params.isDeterministic = True #if true, nShots option is rendered useless
    params.maxIters = 1  # initial energy only - no internal optimisation steps
    params.nQubits = 2 # Number of qubits
    params.pauliString = "-83.25725311170572  + -0.5717771747923628 Z0 + -0.1764363062038683 Z1 + -0.14683081784108865 Z0Z1 + -0.05765562087249825 Z0X1 + -0.0065847942276541505 X0Z1 + 0.01980854363989911 Y0Y1 + 0.05765562087249792 X1 + 0.07532333439618966 X0 + 0.08878182442061067 X0X1"
    params.circuitString = '''
.compiler xasm 
.circuit ansatz
.parameters theta
.qbit q
    Ry(q[0], theta[0]);
    Ry(q[1], theta[1]);
    CNOT(q[0], q[1]);
    Ry(q[1], theta[2]);
'''
    params.optimalParameters = theta #set parameters
    vqe = qbOptVqe.VQEE(params)
    vqe.run()
    return params.optimalValue

#(2) connect to optimizer and print results
theta = np.array([0.0, 0.0, 0.0]) #initial guess
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
                
#(3) optional: use pyscf to get reference energies
from pyscf import gto, scf, ci, fci

#(3.2) do SCF
mf = scf.RHF(mol)
mf.conv_tol = 1e-12
mf.conv_tol_grad = 1e-12
mf.max_cycle = 100
mf.kernel()
escf = mf.e_tot

#(3.3) do FCI
fcisolver = fci.FCI(mf)
fcisolver.conv_tol = 1e-12
efci = fcisolver.kernel()[0]

#(3.4) do frozen CISD to compare to VQE
cisolver = ci.CISD(mf,  frozen = [0,1,2,4]) #this should yield the exact same energy as the VQE
cisolver.conv_tol = 1e-12
eci = cisolver.kernel()[0] + mf.e_tot
print("done!")

#(4) print results
print("---------------------------")
print("{:>11} | {:>16}".format('Method','Energy [a.u.]'))
print("---------------------------")
print("{0:<11} | {1:>16.12f}".format('Nuc. rep.', enuc))
print("{0:<11} | {1:>16.12f}".format('SCF', escf))
print("{0:<11} | {1:>16.12f}".format('FCI (exact)', efci))
print("{0:<11} | {1:>16.12f}".format('frozen FCI', eci))
print("{0:<11} | {1:>16.12f}".format('VQE', evqe + enuc))
