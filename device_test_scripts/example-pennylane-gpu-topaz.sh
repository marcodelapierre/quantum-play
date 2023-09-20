#!/bin/bash

# GPU case

# Slurm interactive session - Topaz
# salloc -N 1 -n 2 -c 8 --gres=gpu:2 -p gpuq-dev -t 30:00

# gpu offloading
srun --exact -n 1 -c 1 --gres=gpu:1 ./test-rotation-pennylane-lightning-gpu.py

# mpi test from github repo
cd pennylane-lightning-gpu/mpitests
srun --exact --gres=gpu:2 -n 2 -c 1 python -m pytest test_apply.py
