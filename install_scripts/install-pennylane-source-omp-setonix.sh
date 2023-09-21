#!/bin/bash

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $script_dir/use-pennylane-source-omp-setonix.sh

# install from source
git clone https://github.com/PennyLaneAI/pennylane-lightning-kokkos $source_dir/pennylane-lightning-kokkos
cd $source_dir/pennylane-lightning-kokkos
git checkout v$pl_ver

CMAKE_ARGS="-DCMAKE_CXX_COMPILER=CC \
  -DCMAKE_BUILD_TYPE=Release \
  -DPLKOKKOS_ENABLE_NATIVE=ON \
  -DKokkos_ENABLE_OPENMP=ON \
  -DKokkos_ARCH_ZEN3=On" \
  pip install --prefix=$install_dir .

cd -
