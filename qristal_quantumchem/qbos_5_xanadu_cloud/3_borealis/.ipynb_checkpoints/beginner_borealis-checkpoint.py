#!/usr/bin/env python3

import strawberryfields as sf
import numpy as np

eng = sf.RemoteEngine("borealis")
device = eng.device

device.certificate

from strawberryfields.tdm import borealis_gbs, full_compile, get_mode_indices

gate_args_list = borealis_gbs(device, modes=216, squeezing="high")

delays = [1, 6, 36]
vac_modes = sum(delays)

n, N = get_mode_indices(delays)

from strawberryfields.ops import Sgate, Rgate, BSgate, MeasureFock

prog = sf.TDMProgram(N)

with prog.context(*gate_args_list) as (p, q):
    Sgate(p[0]) | q[n[0]]
    for i in range(len(delays)):
        Rgate(p[2 * i + 1]) | q[n[i]]
        BSgate(p[2 * i + 2], np.pi / 2) | (q[n[i + 1]], q[n[i]])
    MeasureFock() | q[0]

shots = 250_000
results = eng.run(prog, shots=shots, crop=True)

samples = results.samples

from strawberryfields.utils import gbs_sample_runtime

runtimes = np.array([gbs_sample_runtime(sample[0]) for sample in samples])

import matplotlib.pyplot as plt

fs_axlabel = 22
fs_text = 20
fs_ticklabel = 21
fs_legend = 20


def plot_simulation_time(runtimes):
    """Plots a histogram with simulation times.

    Args:
        runtimes (array[float]): the runtimes per GBS sample
    """
    runtimes_log_years = np.log10(runtimes / 365 / 24 / 3600)
    max_exponent = int(max(runtimes_log_years))
    min_exponent = int(min(runtimes_log_years))

    _, ax = plt.subplots(figsize=(18, 8))
    bins = np.arange(min_exponent, max_exponent + 1)
    ax.hist(runtimes_log_years, width=0.8, bins=bins - 0.4)
    ax.set_xlabel(r"simulation time [log$_{10}$ years]", fontsize=fs_axlabel)
    ax.set_ylabel("occurrence", fontsize=fs_axlabel)
    ax.set_yscale("log")
    ax.tick_params(axis="x", labelsize=fs_ticklabel)
    ax.tick_params(axis="y", labelsize=fs_ticklabel)
    ax.set_xticks(bins)

    plt.savefig("simul_time.png")


plot_simulation_time(runtimes)

runtime_data = f"""
simulation runtimes [years]
median: {np.median(runtimes) / 365 / 24 / 3600:.1E}
average: {np.mean(runtimes) / 365 / 24 / 3600:.1E}
brightest: {np.max(runtimes) / 365 / 24 / 3600:.1E}
total: {np.sum(runtimes) / 365 / 24 / 3600:.1E}
"""

print(runtime_data)

mean_n = np.mean(samples, axis=(0, 1))
cov_n = np.cov(samples[:, 0, :].T)

import matplotlib.colors


def plot_photon_number_moments(mean_n, cov_n, file):
    """Plots first and second moment of the photon-number distribution.

    Args:
        mean_n (array[float]): mean photon number per mode
        cov_n (array[int]): photon-number covariance matrix
    """
    _, ax = plt.subplots(1, 2, figsize=(18, 8))

    ax[0].bar(range(len(mean_n)), mean_n, width=0.75, align="center")
    ax[0].set_title(
        rf"<$n$> = {np.mean(mean_n):.3f}, <$N$> = {np.sum(mean_n):.3f}",
        fontsize=fs_axlabel,
    )
    ax[0].set_xlabel("pulse index", fontsize=fs_axlabel)
    ax[0].set_ylabel("mean photon number", fontsize=fs_axlabel)
    ax[0].grid()
    ax[0].tick_params(axis="x", labelsize=fs_ticklabel)
    ax[0].tick_params(axis="y", labelsize=fs_ticklabel)

    ax[1].imshow(
        cov_n,
        norm=matplotlib.colors.SymLogNorm(
            linthresh=10e-6, linscale=1e-4, vmin=0, vmax=2
        ),
        cmap="rainbow",
    )
    ax[1].set_title(r"Cov($n{_i}$, $n{_j}$)", fontsize=fs_axlabel)
    ax[1].tick_params(axis="x", labelsize=fs_ticklabel)
    ax[1].tick_params(axis="y", labelsize=fs_ticklabel)

    plt.savefig(file)


plot_photon_number_moments(mean_n, cov_n, "photon_number_dist.png")

compile_options = {
    "device": device,
    "realistic_loss": True,
}

run_options = {
    "shots": None,
    "crop": True,
    "space_unroll": True,
}

eng_sim = sf.Engine(backend="gaussian")
results_sim = eng_sim.run(prog, **run_options, compile_options=compile_options)

cov = results_sim.state.cov()

from thewalrus.quantum import (
    photon_number_mean_vector,
    photon_number_covmat,
)

mu = np.zeros(len(cov))
mean_n_sim = photon_number_mean_vector(mu, cov)
cov_n_sim = photon_number_covmat(mu, cov)

plot_photon_number_moments(mean_n_sim, cov_n_sim, "photon_number_dist_2.png")

def plot_photon_number_moment_comparison(mean_n_exp, mean_n_sim, cov_n_exp, cov_n_sim):
    """Plot first and second moment of the PNR distribution.

    Compare in scatter plots the first and second moments of the photon-number
    distribution resulting from experiment and simulation.

    Args:
        mean_n_exp (array): experimental mean photon number per mode
        mean_n_sim (array): simulated mean photon number per mode
        cov_n_exp (array): experimental photon-number covariance matrix
        cov_n_sim (array): simulated photon-number covariance matrix
    """
    cov_n_exp2 = np.copy(cov_n_exp)
    cov_n_sim2 = np.copy(cov_n_sim)

    # remove the diagonal elements (corresponding to the single-mode variance)
    # which would otherwise be dominant
    cov_n_exp2 -= np.diag(np.diag(cov_n_exp2))
    cov_n_sim2 -= np.diag(np.diag(cov_n_sim2))

    _, ax = plt.subplots(1, 2, figsize=(18, 8))

    min_ = np.min([mean_n_sim, mean_n_exp])
    max_ = np.max([mean_n_sim, mean_n_exp])
    ax[0].scatter(mean_n_sim, mean_n_exp, s=4, alpha=0.50)
    ax[0].plot([min_, max_], [min_, max_], "k--")
    ax[0].set_title("1st moment", fontsize=fs_axlabel)
    ax[0].set_xlabel("simulation", fontsize=fs_axlabel)
    ax[0].set_ylabel("experiment", fontsize=fs_axlabel)
    ax[0].set_xlim([min_, max_])
    ax[0].set_ylim([min_, max_])
    ax[0].set_aspect("equal", adjustable="box")
    ax[0].tick_params(axis="x", labelsize=fs_ticklabel)
    ax[0].tick_params(axis="y", labelsize=fs_ticklabel)
    ax[0].grid()

    min_ = np.min([cov_n_sim2, cov_n_exp2])
    max_ = np.max([cov_n_sim2, cov_n_exp2])
    ax[1].scatter(cov_n_sim2, cov_n_exp2, s=4, alpha=0.50)
    ax[1].plot([min_, max_], [min_, max_], "k--")
    ax[1].set_title("2nd moment", fontsize=fs_axlabel)
    ax[1].set_xlabel("simulation", fontsize=fs_axlabel)
    ax[1].set_ylabel("experiment", fontsize=fs_axlabel)
    ax[1].set_xlim([min_, max_])
    ax[1].set_ylim([min_, max_])
    ax[1].set_aspect("equal", adjustable="box")
    ax[1].tick_params(axis="x", labelsize=fs_ticklabel)
    ax[1].tick_params(axis="y", labelsize=fs_ticklabel)
    ax[1].grid()

    plt.savefig("photon_number_compare.png")


plot_photon_number_moment_comparison(mean_n, mean_n_sim, cov_n, cov_n_sim)

