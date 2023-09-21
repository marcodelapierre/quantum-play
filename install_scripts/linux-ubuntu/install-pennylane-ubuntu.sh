#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $script_dir/use-pennylane-ubuntu.sh

# install pre-requisites
sudo apt-get update
sudo apt-get install -y \
  python3 \
  python3-pip \
  python3-setuptools
pip3 install --upgrade pip

# install
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  pennylane=="$pl_ver" \
  pennylane-lightning=="$pl_ver" \
  pennylane-lightning-kokkos=="$pl_ver"

# configure for startup
echo "export PYTHONPATH=\"$lib_dir:\$PYTHONPATH\"" >> $(eval echo ~${USERID})/.bashrc
echo "export PATH=\"$bin_dir:\$PATH\"" >> $(eval echo ~${USERID})/.bashrc

