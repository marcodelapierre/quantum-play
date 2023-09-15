#!/bin/bash

module load python/3.10.10
module load py-pip/23.1.2-py3.10.10
module load cmake/3.24.3
module load eigen/3.4.0
module load openblas/0.3.21

export WORKING_DIR="$(pwd)"
export SOURCE_DIR="${WORKING_DIR}/source"
export INSTALL_DIR="${WORKING_DIR}/install"
export PIP_DIR="${WORKING_DIR}/pip"

export PATH="${PIP_DIR}/bin:$PATH"
export PYTHONPATH="${PIP_DIR}/lib/python3.10/site-packages:$PYTHONPATH"

export PYTHONPATH="${INSTALL_DIR}/qristal-local/lib:$PYTHONPATH"
