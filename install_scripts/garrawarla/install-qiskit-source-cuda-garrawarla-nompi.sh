#!/bin/bash -l
#SBATCH --job-name=install-qiskit-source-cuda-garrawarla-nompi
#SBATCH --account=pawsey0001
#SBATCH --partition=gpuq-dev
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=out-%x

script_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $script_dir/use-qiskit-source-cuda-garrawarla-nompi.sh

# install
git clone https://github.com/Qiskit/qiskit-aer $source_dir/qiskit-aer
cd $source_dir/qiskit-aer
git checkout $aer_ver
pip install --prefix=$install_dir -r requirements-dev.txt
pip install --prefix=$install_dir pybind11[global]

pip install --prefix=$install_dir nvidia-cuda-runtime-cu11 nvidia-cublas-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11 cuquantum-cu11

python ./setup.py bdist_wheel -- \
  -DCMAKE_BUILD_TYPE=Release \
  -DAER_MPI=False \
  -DAER_THRUST_BACKEND=CUDA \
  -DAER_CUDA_ARCH=7.0 \
  -DAER_DISABLE_GDR=False \
  -AER_PYTHON_CUDA_ROOT=$install_dir \
  --

pip install --prefix=$install_dir dist/qiskit_aer*.whl
cd -
