#!/bin/bash

export HERE="$(pwd)"
. use-qristal.sh

mkdir -p "${SOURCE_DIR}"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${PIP_DIR}"

# Install required dependencies
# TODO: try and skip it
cd $SOURCE_DIR
rm -rf boost_1_71_0
wget https://boostorg.jfrog.io/artifactory/main/release/1.71.0/source/boost_1_71_0.tar.bz2
tar --bzip2 -xf boost_1_71_0.tar.bz2
cd boost_1_71_0/
./bootstrap.sh --prefix=${INSTALL_DIR}/boost-local
./b2 install
#
python3 -m pip install ipopo --prefix="${PIP_DIR}"
python3 -m pip install pyscf --prefix="${PIP_DIR}"
#export PATH="${PIP_DIR}/bin:$PATH"
#export PYTHONPATH="${PIP_DIR}/lib/python3.10/site-packages:$PYTHONPATH"

# Install Qristal
cd $SOURCE_DIR
git clone https://gitlab.com/qbau/software-and-apps/public/QBSDK.git
cd QBSDK
mkdir build && cd build
cmake .. \
  -DINSTALL_MISSING=ON \
  -DENABLE_MPI=ON \
  -DBOOST_ROOT=${INSTALL_DIR}/boost-local \
  -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR}/qristal-local \
  -DCMAKE_CXX_FLAGS="-I${INSTALL_DIR}/boost-local/include" \
  -DCMAKE_INSTALL_LIBDIR=lib
# workaround for lib/lib64 in line above

#
make -j8 install
#export PYTHONPATH="${INSTALL_DIR}/qristal-local/lib:$PYTHONPATH"

cd $HERE
./test-qristal.py

# one-off config change
# print(tqb.qpu_configs)
# for the qdk entry: https://xxx.xxx.yy.yy:8443/api/v1/


