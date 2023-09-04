#!/usr/bin/env python3

from strawberryfields.apps import data, qchem
import numpy as np


formic = data.Formic()
w = formic.w  # ground state frequencies
wp = formic.wp  # excited state frequencies
Ud = formic.Ud  # Duschinsky matrix
delta = formic.delta  # displacement vector
T = 0  # temperature

t, U1, r, U2, alpha = qchem.vibronic.gbs_params(w, wp, Ud, delta, T)

e = qchem.vibronic.energies(formic, w, wp)
print(np.around(e[:5], 4))  # 4 decimal precision

from strawberryfields.apps import plot

nr_samples = 10

s = qchem.vibronic.sample(t, U1, r, U2, alpha, nr_samples)
e = qchem.vibronic.energies(s, w, wp)
plot.spectrum(e, xmin=-1000, xmax=8000)

e = qchem.vibronic.energies(formic, w, wp)
plot.spectrum(e, xmin=-1000, xmax=8000)
