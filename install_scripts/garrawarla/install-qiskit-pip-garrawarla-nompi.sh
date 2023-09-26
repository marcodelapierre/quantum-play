#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $script_dir/use-qiskit-pip-garrawarla-nompi.sh

# install
mkdir -p $install_dir
pip install --prefix="$install_dir" \
  qiskit=="$qk_ver" \
  qiskit-aer-gpu-cu11=="$aer_ver"
