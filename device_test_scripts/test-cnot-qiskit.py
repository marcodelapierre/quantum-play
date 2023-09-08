#!/usr/bin/env python3

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile

def create_circuit():
    circ = QuantumCircuit(3)
    circ.h(0)
    circ.cx(0, 1)
    circ.cx(0, 2)
    return circ


# build and visualise a circuit
circ = create_circuit()
circ.save_statevector()

circ.draw('text')

# Run the quantum circuit on the Aer statevector simulator backend
backend = AerSimulator(method='statevector')
circ = transpile(circ, backend)

job = backend.run(circ)
result = job.result()

outputstate = result.get_statevector(circ, decimals=3)
print(outputstate)


# rebuild circuit for unitary method
circ = create_circuit()
circ.save_unitary()

# Run the quantum circuit on the Aer unitary simulator backend
backend = AerSimulator(method='unitary')
circ = transpile(circ, backend)

job = backend.run(circ)
result = job.result()

outputstate = result.get_unitary(circ, decimals=3)
print(outputstate)




# create a quantum circuit with measurements
circ = create_circuit()
meas = QuantumCircuit(3, 3)
meas.barrier(range(3))
meas.measure(range(3), range(3))

circ.add_register(meas.cregs[0])
qc = circ.compose(meas)

qc.draw('text')

# Run the quantum circuit on the automatic Aer backend
backend = AerSimulator()
circ = transpile(qc, backend)

job = backend.run(circ, shots=1024)
result = job.result()

counts = result.get_counts(qc)
print(counts)

