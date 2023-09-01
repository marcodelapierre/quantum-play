#!/bin/bash

# essential for reproducibility of installation
tool_name="qiskit"
qk_ver="0.44.1"
aer_ver="0.12.2"

# install pre-requisites
sudo apt-get update
sudo apt-get install -y \
  python3 \
  python3-pip \
  python3-setuptools
pip3 install --upgrade pip

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
lib_dir="$install_dir/local/lib/python${python_ver}/dist-packages"
bin_dir="$install_dir/local/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH" 
export PATH="$bin_dir:$PATH"

# install
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  qiskit="$qk_ver" \
  qiskit-aer="$aer_ver"

# configure for startup
echo "export PYTHONPATH=\"$lib_dir:\$PYTHONPATH\"" >> $(eval echo ~${USERID})/.bashrc
echo "export PATH=\"$bin_dir:\$PATH\"" >> $(eval echo ~${USERID})/.bashrc

