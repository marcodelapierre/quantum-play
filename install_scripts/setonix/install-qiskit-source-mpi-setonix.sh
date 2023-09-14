#!/bin/bash

. use-qiskit-source-mpi-setonix.sh

# install
git clone https://github.com/Qiskit/qiskit-aer $source_dir/qiskit-aer
cd $source_dir/qiskit-aer
git checkout $aer_ver
pip install --prefix=$install_dir -r requirements-dev.txt

CMAKE_ARGS="-DCMAKE_CXX_COMPILER=CC \
  -DCMAKE_BUILD_TYPE=Release \
  -DAER_MPI=True \
  -DAER_DISABLE_GDR=True" \
  pip install --prefix=$install_dir .
#  -DAER_BLAS_LIB_PATH=$PAWSEY_OPENBLAS_HOME \
#  -DAER_THRUST_BACKEND=OMP \

cd -
