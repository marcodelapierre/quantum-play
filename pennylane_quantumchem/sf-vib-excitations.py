#!/usr/bin/env python3

import numpy as np
import strawberryfields as sf
from strawberryfields.apps import qchem
import matplotlib.pyplot as plt


Li = sf.apps.data.Pyrrole(0).Li  # normal modes of the ground electronic state
Lf = sf.apps.data.Pyrrole(0).Lf  # normal modes of the excited electronic state
ri = sf.apps.data.Pyrrole(0).ri  # atomic coordinates of the ground electronic state
rf = sf.apps.data.Pyrrole(0).rf  # atomic coordinates of the excited electronic state
wi = sf.apps.data.Pyrrole(0).wi  # vibrational frequencies of the ground electronic state
wf = sf.apps.data.Pyrrole(0).wf  # vibrational frequencies of the excited electronic state
m = sf.apps.data.Pyrrole(0).m  # atomic masses

Ud, delta = qchem.duschinsky(Li, Lf, ri, rf, wf, m)

plt.imshow(abs(Ud), cmap="Greens")
plt.colorbar()
plt.xlabel("Mode index")
plt.ylabel("Mode index")
plt.tight_layout()
plt.savefig("matrix.png")

_, U1, r, U2, alpha = qchem.vibronic.gbs_params(wi, wf, Ud, delta)

np.random.seed(seed=1919)
n_samples = 5
n_modes = len(alpha)
eng = sf.LocalEngine(backend="gaussian")
gbs = sf.Program(n_modes)

with gbs.context as q:
    qchem.vibronic.VibronicTransition(U1, r, U2, alpha) | q
    sf.ops.MeasureFock() | q
samples = eng.run(gbs, shots=n_samples).samples.tolist()

n_mean = np.mean(samples, axis=0)

plt.figure(figsize=(8, 4))
plt.ylabel("Mean photon number")
plt.xlabel(r"Frequency (cm$^{-1}$)")
plt.xticks(range(len(wf)), np.round(wf, 1), rotation=90)
plt.bar(range(len(wf)), n_mean, color="green")
plt.tight_layout()
plt.savefig("ave_quanta.png")

np.random.seed(seed=1919)
n_samples = 5
n_modes = len(alpha)
eng = sf.LocalEngine(backend="gaussian")
gbs = sf.Program(n_modes)

with gbs.context as q:
    sf.ops.Dgate(1) | q[19]
    qchem.vibronic.VibronicTransition(U1, r, U2, alpha) | q
    sf.ops.MeasureFock() | q
samples = eng.run(gbs, shots=n_samples).samples.tolist()

fig, ax = plt.subplots(figsize=(8, 4))
plt.ylabel("Mean photon number")
plt.xlabel(r"Frequency (cm$^{-1}$)")
plt.ylim(-1.1, 1.1)
ax.set_yticklabels([(abs(tick)) for tick in np.round(ax.get_yticks(), 1)])
ax.axhline(0, color="black", lw=0.5)
plt.xticks(range(len(wf)), np.round(wf, 1), rotation=90)
plt.bar(range(len(wf)), n_mean, color="green", label=("input state is pre-excited"))
plt.xticks(range(len(wf)), np.round(wf, 1), rotation=90)
plt.bar(range(len(wf)), -n_mean, color="green", alpha=0.4, label=("no pre-excitation"))
plt.legend(frameon=False, loc=2)
plt.tight_layout()
plt.savefig("ave_photons.png")

