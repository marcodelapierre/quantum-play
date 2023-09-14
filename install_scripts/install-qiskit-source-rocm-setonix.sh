#!/bin/bash

. use-qiskit-source-rocm-setonix.sh

# install
git clone https://github.com/Qiskit/qiskit-aer $source_dir/qiskit-aer
cd $source_dir/qiskit-aer
git checkout $aer_ver
pip install --prefix=$install_dir -r requirements-dev.txt
pip install --prefix=$install_dir pybind11[global]

python ./setup.py bdist_wheel -- \
  -DCMAKE_CXX_COMPILER=hipcc \
  -DCMAKE_BUILD_TYPE=Release \
  -DAER_MPI=True \
  -DAER_THRUST_BACKEND=ROCM \
  -DAER_ROCM_ARCH=gfx90a \
  -DAER_DISABLE_GDR=False \
  --

pip install --prefix=$install_dir dist/qiskit_aer*.whl
cd -
