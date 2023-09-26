#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $script_dir/CRASH-use-pennylane-pip-garrawarla-nompi.sh

# install
# this will get Lightning with Nvidia GPU backend
mkdir -p $install_dir
pip install --prefix="$install_dir" nvidia-cuda-runtime-cu11 nvidia-cublas-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11 cuquantum-cu11
pip install --prefix="$install_dir" \
  pennylane=="$pl_ver" \
  pennylane-lightning=="$pl_ver" \
  pennylane-lightning-gpu=="$pl_ver"
