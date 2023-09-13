#!/bin/bash

# essential for reproducibility of installation
tool_name="pennylane"
pl_ver="0.32.0"

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
lib_dir="$install_dir/local/lib/python${python_ver}/dist-packages"
bin_dir="$install_dir/local/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH"
export PATH="$bin_dir:$PATH"

