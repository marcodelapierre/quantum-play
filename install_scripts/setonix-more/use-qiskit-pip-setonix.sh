#!/bin/bash

# essential for reproducibility of installation
tool_name="qiskit-pip"
qk_ver="0.44.1"
aer_ver="0.12.2"

# host versions
py_ver="3.10.10"
pip_ver="23.1.2-py3.10.10"

# load modules
module load python/$py_ver
module load py-pip/$pip_ver

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
lib_dir="$install_dir/lib/python${python_ver}/site-packages"
bin_dir="$install_dir/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH"
export PATH="$bin_dir:$PATH"
