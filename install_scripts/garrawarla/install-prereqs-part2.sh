#!/bin/bash -l
#SBATCH --job-name=install-qiskit-source-cuda-garrawarla
#SBATCH --account=pawsey0001
#SBATCH --partition=gpuq-dev
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=out-%x

# has to be run from the quantum-play repo, subdir install_scripts/garrawarla/

py_ver="3.10.10"
pip_ver="23.1.2"
st_ver="68.0.0"

module load maali/1.8.4
mkdir -p $MYASTRO/software/mwa_sles12sp5/modulefiles
module use $MYASTRO/software/mwa_sles12sp5/modulefiles
module swap gcc gcc/8.3.0

# requires Cuda driver directory (gpuq node)
maali -t gdrcopy -v 1.3 -n

maali -t ucx -v 1.6.0 -n
maali -t openmpi-ucx -v 4.0.3 -n
