#!/bin/bash

# essential for reproducibility of installation
tool_name="qiskit"
qk_ver="0.44.1"
aer_ver="0.12.2"

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
install_dir="$script_dir/$tool_name"
lib_dir="$install_dir/local/lib/python${python_ver}/dist-packages"
bin_dir="$install_dir/local/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH"
export PATH="$bin_dir:$PATH"

