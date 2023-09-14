#!/bin/bash

. use-qiskit-pip-setonix.sh

# install
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  qiskit=="$qk_ver" \
  qiskit-aer=="$aer_ver"
