#!/bin/bash

. use-pennylane-source-omp-setonix.sh

# install from source
git clone https://github.com/PennyLaneAI/pennylane-lightning-kokkos $source_dir/pennylane-lightning-kokkos
cd $source_dir/pennylane-lightning-kokkos
git checkout v$pl_ver
CMAKE_ARGS="-DCMAKE_CXX_COMPILER=CC \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH=$install_dir \
  -DPLKOKKOS_ENABLE_NATIVE=ON \
  -DKokkos_ENABLE_OPENMP=ON" \
  pip install --prefix=$install_dir .
cd -

# configure for startup
echo "export PYTHONPATH=\"$lib_dir:\$PYTHONPATH\"" >> $(eval echo ~${USERID})/.bashrc
echo "export PATH=\"$bin_dir:\$PATH\"" >> $(eval echo ~${USERID})/.bashrc

