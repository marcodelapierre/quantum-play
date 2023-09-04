#!/usr/bin/env python3
from prepare_library import *


from pyscf import gto, scf

#(1) define molecule
mol = gto.Mole()
mol.build(
        atom = '''Li 0 0 -2.525; Li 0 0 +2.525''',
        unit = 'B',
        basis = 'sto-3g',
        symmetry = 'Dooh'
        )

#(2) do Hartree-Fock calculation and obtain MO integrals  
mf = scf.RHF(mol)
mf.conv_tol = 1e-14
mf.conv_tol_grad = 1e-14
mf.max_cycle = 200
mf.kernel()

#print orbital energies, occupancies and irreps
mf.analyze()


#quit()
## analyse the output of `mf.analyze()` above,
## to choose which configurations to add to the `mpb` object below


mpb = [ConfigurationStateFunction.from_str({"0+0-1+1-2+2-" : 1.0}),
       ConfigurationStateFunction.from_str({"0+0-1+1-4+4-" : 1.0}),
       ConfigurationStateFunction.from_str({"0+0-1+1-5+5-" : 1.0}),
       ConfigurationStateFunction.from_str({"0+0-1+1-9+9-" : 1.0})]

print("Many-particle basis:")
for i in mpb:
    print(i)


from pyscf import ao2mo
from functools import reduce

#do ao -> mo transformation 
h1ao = scf.hf.get_hcore(mol) #get 1p AO integrals 
h1mo = reduce(np.dot, (mf.mo_coeff.T, h1ao, mf.mo_coeff)) #transform to MO basis 
h2mo = ao2mo.full(mol, mf.mo_coeff) #get 2p MO integrals


H = np.ndarray([len(mpb), len(mpb)], dtype=np.float64)
for i in range(0, len(mpb), 1):
    for j in range(i, len(mpb), 1):
        H[i,j] = slater_condon_rules_csf(mpb[i], mpb[j], h1mo, h2mo)
        H[j,i] = H[i,j] #use hermiticity
np.set_printoptions(precision=14, suppress=True)
print("Hamiltonian matrix representation:")
print(H)


import pennylane as qml

#do all replacements from dictionary
def replace_all(text:str, dic)->str:
    for before, after in dic.items():
        text = text.replace(before, after)
    return text

#convert hamiltonian to Pauli strings using pennylane
def pauli_decomposition(H) ->str:
    coeffs, obs_list = qml.utils.decompose_hamiltonian(H) #call decomposition routine 
    hamiltonian = qml.Hamiltonian(coeffs, obs_list, simplify = True)
    pauli_string = str(hamiltonian)
    #make string compatible to qbos 
    replacements = {"\n" : "",
                    "[" : "",
                    "]" : "",
                    "(" : "",
                    ")" : "",
                    "I0" : ""}
    pauli_string = replace_all(pauli_string, replacements)
    return pauli_string

pauli_string = pauli_decomposition(H)
print("Pauli string (compatible with qbOS):")
print(pauli_string)
