#!/bin/bash

# has to be run from the quantum-play repo, subdir install_scripts/garrawarla/

py_ver="3.10.10"
pip_ver="23.1.2"
st_ver="68.0.0"

module load maali/1.8.4
mkdir -p $MYASTRO/software/mwa_sles12sp5/modulefiles
module use $MYASTRO/software/mwa_sles12sp5/modulefiles
module swap gcc gcc/8.3.0

sed -i "s;\"setuptools/.*\";\"setuptools/$st_ver\";g" pip.cyg

maali -t libffi  -v 3.0.13
maali -t openssl -v 1.1.1k
maali -t sqlite  -v 3.7.17

maali -t Python -v $py_ver
export MAALI_DEFAULT_PYTHON=python/$py_ver

maali -t setuptools -v $st_ver
maali -t pip -v $pip_ver

maali -t openblas -v 0.3.24
maali -t cmake -v 3.26.0

maali -t gcc -v 11.1.0
