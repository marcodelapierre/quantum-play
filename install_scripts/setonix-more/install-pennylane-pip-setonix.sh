#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $script_dir/use-pennylane-pip-setonix.sh

# install
# this will get kokkos with OpenMP backend
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  pennylane=="$pl_ver" \
  pennylane-lightning=="$pl_ver" \
  pennylane-lightning-kokkos=="$pl_ver"
