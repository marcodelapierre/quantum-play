#!/bin/bash

# essential for reproducibility of installation
tool_name="qiskit-cuda"
#qk_ver="0.44.1"
aer_ver="0.12.2"

# host versions
py_ver=""
pip_ver=""
st_ver=""
blas_ver=""
cuda_ver="11.4.2"
mpi_ver="4.0.2"

# load modules
module load python/$py_ver
module load py-pip/$pip_ver
module load py-setuptools/$st_ver
module load openblas/$blas_ver
module load cuda/$cuda_ver
module load openmpi-ucx-gpu/$mpi_ver

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
source_dir="${install_dir}-src"
lib_dir="$install_dir/lib/python${python_ver}/site-packages"
bin_dir="$install_dir/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH"
export PATH="$bin_dir:$PATH"
