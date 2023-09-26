#!/bin/bash

# essential for reproducibility of installation
# pennylane versions
tool_name="pennylane-cuda-nompi"
pl_ver="0.32.0"
# host versions
gcc_ver="10.1.0"
py_ver="3.10.10"
pip_ver="23.1.2"
st_ver="68.0.0"
cuda_ver="11.4.2"
cmake_ver="3.26.0"

# load modules
module use $MYASTRO/software/mwa_sles12sp5/modulefiles
module swap gcc gcc/$gcc_ver
module load python/$py_ver
module load pip/$pip_ver
module load setuptools/$st_ver
module load cuda/$cuda_ver
module load cmake/$cmake_ver

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
install_dir="$script_dir/$tool_name"
source_dir="${install_dir}-src"
lib_dir="$install_dir/lib/python${python_ver}/site-packages"
bin_dir="$install_dir/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH"
export PATH="$bin_dir:$PATH"
