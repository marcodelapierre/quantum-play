#!/bin/bash

module load py-pip/22.2.2-py3.10.8 python/3.10.8
module load cmake/3.21.4
module load eigen/3.4.0
module load openblas/0.3.15

export WORKING_DIR="/software/projects/pawsey0001/mdelapierre/quantum/qristal-june"
export SOURCE_DIR="${WORKING_DIR}/source"
export INSTALL_DIR="${WORKING_DIR}/install"
export PIP_DIR="${WORKING_DIR}/pip"

export PATH="${PIP_DIR}/bin:$PATH"
export PYTHONPATH="${PIP_DIR}/lib/python3.10/site-packages:$PYTHONPATH"

export PYTHONPATH="${INSTALL_DIR}/qristal-local/lib:$PYTHONPATH"
