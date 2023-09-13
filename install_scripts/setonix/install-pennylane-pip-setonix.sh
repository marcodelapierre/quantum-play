#!/bin/bash

. use-pennylane-pip-setonix.sh

# install
# this will get kokkos with OpenMP backend
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  pennylane=="$pl_ver" \
  pennylane-lightning=="$pl_ver" \
  pennylane-lightning-kokkos=="$pl_ver"

# configure for startup
#echo "export PYTHONPATH=\"$lib_dir:\$PYTHONPATH\"" >> $(eval echo ~${USERID})/.bashrc
#echo "export PATH=\"$bin_dir:\$PATH\"" >> $(eval echo ~${USERID})/.bashrc

