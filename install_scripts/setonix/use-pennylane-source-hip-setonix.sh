#!/bin/bash

# essential for reproducibility of installation
# pennylane versions
tool_name="pennylane-hip"
pl_ver="0.32.0"
# host versions
py_ver="3.10.10"
pip_ver="23.1.2-py3.10.10"
st_ver="68.0.0-py3.10.10"
rocm_ver="5.2.3"

# load modules
module load python/$py_ver
module load py-pip/$pip_ver
module load py-setuptools/$st_ver
module load rocm/$rocm_ver
module load craype-accel-amd-gfx90a

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
source_dir="${install_dir}-src"
lib_dir="$install_dir/lib/python${python_ver}/site-packages"
bin_dir="$install_dir/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH"
export PATH="$bin_dir:$PATH"
