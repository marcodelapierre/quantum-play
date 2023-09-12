#!/bin/bash

# essential for reproducibility of installation
tool_name="pennylane"
pl_ver="0.32.0"

# load modules
module load python/3.10.10
module load py-pip/23.1.2-py3.10.10
module load py-setuptools/68.0.0-py3.10.10

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
lib_dir="$install_dir/lib/python${python_ver}/site-packages"
bin_dir="$install_dir/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH" 
export PATH="$bin_dir:$PATH"

# install
# this will get kokkos with OpenMP backend
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  pennylane=="$pl_ver" \
  pennylane-lightning=="$pl_ver" \
  pennylane-lightning-kokkos=="$pl_ver"

# configure for startup
echo "export PYTHONPATH=\"$lib_dir:\$PYTHONPATH\"" >> $(eval echo ~${USERID})/.bashrc
echo "export PATH=\"$bin_dir:\$PATH\"" >> $(eval echo ~${USERID})/.bashrc

