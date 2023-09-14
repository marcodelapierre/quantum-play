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
