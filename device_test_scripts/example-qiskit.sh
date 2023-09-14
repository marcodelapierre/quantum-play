#!/bin/bash

# Slurm interactive session
# salloc -N 4  --exclusive -p debug -A pawsey0001 --time=10:00

# more memory via mpi
export n=1 ; export c=1 ; export OMP_NUM_THREADS=$c ; srun --exact -N $n -n $n -c $c ./test-volume-qiskit-distributed-mem.py
export n=2 ; export c=1 ; export OMP_NUM_THREADS=$c ; srun --exact -N $n -n $n -c $c ./test-volume-qiskit-distributed-mem.py

# better performance via omp
export n=1 ; export c=1 ; export OMP_NUM_THREADS=$c ; time srun --exact -N $n -n $n -c $c ./test-volume-qiskit-local-big.py
export n=1 ; export c=8 ; export OMP_NUM_THREADS=$c ; time srun --exact -N $n -n $n -c $c ./test-volume-qiskit-local-big.py

# performance with mpi vs omp
export n=1 ; export c=1 ; export OMP_NUM_THREADS=$c ; time srun --exact -N $n -n $n -c $c ./test-volume-qiskit-local-big.py
export n=4 ; export c=1 ; export OMP_NUM_THREADS=$c ; time srun --exact -N $n -n $n -c $c ./test-volume-qiskit-local-big.py
export n=4 ; export c=8 ; export OMP_NUM_THREADS=$c ; time srun --exact -N $n -n $n -c $c ./test-volume-qiskit-local-big.py


# GPU case

# Slurm interactive session
# salloc -N 1 --exclusive --gpus-per-node=8 -p gpu-dev -A pawsey0001-gpu --time=10:00

# gpu offloading
./test-volume-qiskit-gpu-local.py

# more memory via mpi
./test-volume-qiskit-gpu-distributed-mem.py
srun --exact -n 2 --gpus-per-task=1 ./test-volume-qiskit-gpu-distributed-mem.py

# better performance via mpi/multi-gpu
time srun --exact -n 1 --gpus-per-task=1 ./test-volume-qiskit-gpu-distributed-comp.py
time srun --exact -n 2 --gpus-per-task=1 ./test-volume-qiskit-gpu-distributed-comp.py
