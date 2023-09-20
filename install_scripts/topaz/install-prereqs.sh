#!/bin/bash

# has to be run from the quantum-play repo, subdir install_scripts/topaz/

py_ver="3.10.10"
pip_ver="23.1.2"
st_ver="68.0.0"

module load maali/1.8.4
mkdir -p $MYGROUP/software/centos7.6/modulefiles
module use $MYGROUP/software/centos7.6/modulefiles

sed -i "s;\"setuptools/.*\";\"setuptools/$st_ver\";g" pip.cyg

maali -t openssl -v 1.1.1k
maali -t libffi -v 3.0.13 -d
mkdir -p $MYGROUP/software/centos7.6/apps/gcc/4.8.5/libffi/3.0.13/include
cp -p \
  $MYGROUP/software/centos7.6/build/libffi-3.0.13/x86_64-unknown-linux-gnu/include/ffi*.h \
  $MYGROUP/software/centos7.6/apps/gcc/4.8.5/libffi/3.0.13/include/

maali -t Python -v $py_ver
export MAALI_DEFAULT_PYTHON=python/$py_ver

maali -t setuptools -v $st_ver
maali -t pip -v $pip_ver
