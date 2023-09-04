#!/usr/bin/env python3

from strawberryfields.utils import random_interferometer

import strawberryfields as sf
from strawberryfields import ops

from strawberryfields import RemoteEngine

from sympy.utilities.iterables import multiset_permutations
from strawberryfields.apps.similarity import orbits
import numpy as np

from strawberryfields.apps.sample import postselect

U_vibronic = np.array([
    [-0.5349105592386603, 0.8382670887228271, 0.10356058421030308, -0.021311662937477004],
    [-0.6795134137271818, -0.4999083619063322, 0.5369830827402383, 0.001522863010877817],
    [-0.4295084785810517, -0.17320833713971984, -0.7062800928050401, 0.5354341876268153],
    [0.2601051345260338, 0.13190447151471643, 0.4495473331653913, 0.8443066531962792]
])

eng = sf.RemoteEngine("X8")

nr_modes = 8
vibronic_prog = sf.Program(nr_modes)

with vibronic_prog.context as q:
    ops.S2gate(1.0) | (q[0], q[4])

    ops.Interferometer(U_vibronic) | (q[0], q[1], q[2], q[3])
    ops.Interferometer(U_vibronic) | (q[4], q[5], q[6], q[7])

    ops.MeasureFock() | q

vibronic_results = eng.run(vibronic_prog, shots=400000)
vibronic_samples = vibronic_results.samples

from strawberryfields.apps import vibronic, plot
import plotly

vibronic_samples = [list(s) for s in vibronic_samples]

# frequencies of the initial and final normal modes
w = [2979, 1580, 1286, 977]
wp = [2828, 1398, 1227, 855]
energies = vibronic.energies(vibronic_samples, w, wp)

print(vibronic_samples)

plot.spectrum(energies, xmin=-6000, xmax=6000)
