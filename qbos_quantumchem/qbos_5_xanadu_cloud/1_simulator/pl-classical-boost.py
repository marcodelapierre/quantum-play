#!/usr/bin/env python3

import pennylane as qml
from pennylane import qchem
from pennylane import numpy as np


symbols = ["H", "H"]
coordinates = np.array([0.0, 0.0, -0.6614, 0.0, 0.0, 0.6614])
basis_set = "sto-3g"
electrons = 2

H, qubits = qchem.molecular_hamiltonian(
    symbols,
    coordinates,
    basis=basis_set,
)

hf = qchem.hf_state(electrons, qubits)

singles, doubles = qchem.excitations(electrons=electrons, orbitals=qubits)
num_theta = len(singles) + len(doubles)

def circuit_VQE(theta, wires):
    qml.AllSinglesDoubles(
        weights = theta,
        wires = wires,
        hf_state = hf,
        singles = singles,
        doubles = doubles)

dev = qml.device('default.qubit', wires=qubits)
@qml.qnode(dev)
def cost_fn(theta):
    circuit_VQE(theta,range(qubits))
    return qml.expval(H)

stepsize = 0.4
max_iterations = 30
opt = qml.GradientDescentOptimizer(stepsize=stepsize)
theta = np.zeros(num_theta, requires_grad=True)

for n in range(max_iterations):

    theta, prev_energy = opt.step_and_cost(cost_fn, theta)
    samples = cost_fn(theta)

energy_VQE = cost_fn(theta)
theta_opt = theta

print('VQE energy: %.4f' %(energy_VQE))
print('Optimal parameters:', theta_opt)


symbols = ["H", "H"]
coordinates = np.array([0.0, 0.0, -0.6614, 0.0, 0.0, 0.6614])
basis_set = "sto-3g"

H, qubits = qchem.molecular_hamiltonian(
    symbols,
    coordinates,
    basis=basis_set,
)

hf_state = qchem.hf_state(electrons, qubits)
fermionic_Hamiltonian = qml.utils.sparse_hamiltonian(H).toarray()

# we first convert the HF slater determinant to a string
binary_string = ''.join([str(i) for i in hf_state])
# we then obtain the integer corresponding to its binary representation
idx0 = int(binary_string, 2)
# finally we access the entry that corresponds to the HF energy
H11 = fermionic_Hamiltonian[idx0][idx0]
S11 = 1

H22 = energy_VQE
S22 = 1

wires = range(qubits + 1)
dev = qml.device("default.qubit", wires=wires)

@qml.qnode(dev)
def hadamard_test(Uq, Ucl, component='real'):

    if component == 'imag':
        qml.RX(math.pi/2, wires=wires[1:])

    qml.Hadamard(wires=[0])
    qml.ControlledQubitUnitary(Uq.conjugate().T @ Ucl, control_wires=[0], wires=wires[1:])
    qml.Hadamard(wires=[0])

    return qml.probs(wires=[0])

def circuit_product_state(state):
    qml.BasisState(state, range(qubits))

Uq = qml.matrix(circuit_VQE)(theta_opt, range(qubits))

H12 = 0
relevant_basis_states = np.array([[1,1,0,0], [0,1,1,0], [1,0,0,1], [0,0,1,1]], requires_grad=True)
for j, basis_state in enumerate(relevant_basis_states):
    Ucl = qml.matrix(circuit_product_state)(basis_state)
    probs = hadamard_test(Uq, Ucl)
    # The projection Re(<phi_q|i>) corresponds to 2p-1
    y = 2*probs[0]-1
    # We retrieve the quantities <i|H|HF> from the fermionic Hamiltonian
    binary_string = ''.join([str(coeff) for coeff in basis_state])
    idx = int(binary_string, 2)
    overlap_H = fermionic_Hamiltonian[idx0][idx]
    # We sum over all computational basis states
    H12 += y * overlap_H
    # y0 corresponds to Re(<phi_q|HF>)
    if j == 0:
        y0 = y

H21 = np.conjugate(H12)

S12 = y0
S21 = y0.conjugate()

from scipy import linalg

S = np.array([[S11, S12],[S21, S22]])
H = np.array([[H11, H12],[H21, H22]])

evals = linalg.eigvals(H, S)
energy_CBVQE = np.min(evals).real

print('CB-VQE energy %.4f' %(energy_CBVQE))

