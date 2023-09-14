#!/usr/bin/env python3

from qiskit import QuantumCircuit, execute
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.circuit.library import QuantumVolume

sim = AerSimulator(method='statevector', device='CPU', blocking_enable=True, blocking_qubits=20)
circ = QuantumVolume(26, 10, seed = 0)
circ.save_statevector()
circ = transpile(circ)
circ.measure_all()
result = execute(circ, sim, shots=100).result()

if result.to_dict()['metadata']['mpi_rank'] == 0:
    outputstate = result.get_statevector(circ, decimals=3)
    print(outputstate)

    counts = result.get_counts(circ)
    print(counts)
