#!/usr/bin/env python3

import numpy as np
from qiskit import QuantumCircuit, Aer, BasicAer
from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector


# build and visualise a circuit
circ = QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)

circ.draw('text')


# Run the quantum circuit on the Aer statevector simulator backend
backend = Aer.get_backend('statevector_simulator')

job = backend.run(circ)
result = job.result()

outputstate = result.get_statevector(circ, decimals=3)
print(outputstate)


# Run the quantum circuit on the Aer unitary simulator backend
backend = Aer.get_backend('unitary_simulator')

job = backend.run(circ)
result = job.result()

outputstate = result.get_unitary(circ, decimals=3)
print(outputstate)






# create a quantum circuit with measurements
meas = QuantumCircuit(3, 3)
meas.barrier(range(3))
meas.measure(range(3), range(3))

circ.add_register(meas.cregs[0])
qc = circ.compose(meas)

qc.draw('text')


# Run the quantum circuit on the Aer qasm_simulator backend
backend_sim = Aer.get_backend('qasm_simulator')

job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)
result_sim = job_sim.result()

counts = result_sim.get_counts(qc)
print(counts)


# Run the quantum circuit on the BasicAer qasm_simulator backend
backend_sim = BasicAer.get_backend('qasm_simulator')

job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)
result_sim = job_sim.result()

counts = result_sim.get_counts(qc)
print(counts)
