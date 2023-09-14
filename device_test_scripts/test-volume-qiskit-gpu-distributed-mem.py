#!/usr/bin/env python3

from qiskit import QuantumCircuit, execute
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
from qiskit.circuit.library import QuantumVolume

sim = AerSimulator(method='statevector', device='GPU', blocking_enable=True, blocking_qubits=23)
circ = QuantumVolume(34, 10, seed = 0)
circ.save_statevector()
circ = transpile(circ)
circ.measure_all()
result = execute(circ, sim, shots=100).result()

outputstate = result.get_statevector(circ, decimals=3)
print(outputstate)

counts = result.get_counts(circ)
print(counts)
