#!/bin/bash

# has to be run from the quantum-play repo, subdir install_scripts/garrawarla/

py_ver="3.10.10"
pip_ver="23.1.2"
st_ver="68.0.0"

module load maali/1.8.4
mkdir -p $MYASTRO/software/mwa_sles12sp5/modulefiles
module use $MYASTRO/software/mwa_sles12sp5/modulefiles
module swap gcc gcc/8.3.0

maali -t gcc -v 11.1.0
maali -t gdrcopy -v 1.3 -n
maali -t ucx -v 1.6.0 -n
maali -t openmpi-ucx -v 4.0.3 -n
