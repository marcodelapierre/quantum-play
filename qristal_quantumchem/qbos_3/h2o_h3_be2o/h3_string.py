from basic_quantum_chemistry import *

#(1) define molecule
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

#(2) do Hartree-Fock calculation and obtain MO integrals  
mf = scf.RHF(mol)
mf.conv_tol = 1e-14
mf.conv_tol_grad = 1e-14
mf.max_cycle = 100
mf.kernel()

#print orbital energies, occupancies and irreps
mf.analyze()

#define many particle basis
mpb = [ConfigurationStateFunction.from_str({"0+0-1+" : 1.0}),
       ConfigurationStateFunction.from_str({"0+1-2+" : 1.0/np.sqrt(2), 
                                            "0-1+2+" : -1.0/np.sqrt(2)}),
       ConfigurationStateFunction.from_str({"0+1+2-" : 2.0/np.sqrt(6), 
                                            "0+1-2+" : -1.0/np.sqrt(6),
                                            "0-1+2+" : -1.0/np.sqrt(6)}),
       ConfigurationStateFunction.from_str({"1+2+2-" : 1.0})]

print("Many-particle basis:")
for i in mpb:
    print(i)

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

pauli_string = pauli_decomposition(H)
print("Pauli string (compatible with qbOS):")
print(pauli_string)