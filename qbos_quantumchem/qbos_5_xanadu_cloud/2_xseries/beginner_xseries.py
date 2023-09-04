#!/usr/bin/env python3

import numpy as np

import strawberryfields as sf
from strawberryfields import ops
from strawberryfields import RemoteEngine

import xcc.commands
xcc.commands.ping()

from strawberryfields.utils import random_interferometer
U = random_interferometer(4)
np.set_printoptions(precision=16)
print(U)

prog = sf.Program(8, name="remote_job1")

with prog.context as q:
    # Initial squeezed states
    # Allowed values are r=1.0 or r=0.0
    ops.S2gate(1.0) | (q[0], q[4])
    ops.S2gate(1.0) | (q[1], q[5])
    ops.S2gate(1.0) | (q[3], q[7])

    # Interferometer on the signal modes (0-3)
    ops.Interferometer(U) | (q[0], q[1], q[2], q[3])
    ops.BSgate(0.543, 0.123) | (q[2], q[0])
    ops.Rgate(0.453) | q[1]
    ops.MZgate(0.65, -0.54) | (q[2], q[3])

    # *Same* interferometer on the idler modes (4-7)
    ops.Interferometer(U) | (q[4], q[5], q[6], q[7])
    ops.BSgate(0.543, 0.123) | (q[6], q[4])
    ops.Rgate(0.453) | q[5]
    ops.MZgate(0.65, -0.54) | (q[6], q[7])

    ops.MeasureFock() | q

eng = RemoteEngine("X8")

results = eng.run(prog, shots=20)

print(results.samples)

print(np.mean(results.samples, axis=0))

from collections import Counter
bitstrings = [tuple(i) for i in results.samples]
counts = {k:v for k, v in Counter(bitstrings).items()}
print(counts[(0, 0, 0, 0, 0, 0, 0, 0)])

job = eng.run_async(prog, shots=100)

print(job.id)
print(job.status)

job.clear()
job.status()

job.wait()
print(job.status)

result = sf.Result(job.result)
print(result.samples.shape)

prog_compiled = prog.compile(device=eng.device)
prog_compiled.print()

