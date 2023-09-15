#!/bin/bash -l
#SBATCH --job-name=install-qiskit-source-cuda-topaz
#SBATCH --account=pawsey0001-gpu
#SBATCH --partition=gpu-dev
#SBATCH --exclusive
#SBATCH --ntasks=1
#SBATCH --threads-per-core=1
#SBATCH --gpus-per-node=8
#SBATCH --time=00:30:00
#SBATCH --output=out-%x

. use-qiskit-source-cuda-topaz.sh

# install
git clone https://github.com/Qiskit/qiskit-aer $source_dir/qiskit-aer
cd $source_dir/qiskit-aer
git checkout $aer_ver
pip install --prefix=$install_dir -r requirements-dev.txt
pip install --prefix=$install_dir pybind11[global]

pip install nvidia-cuda-runtime-cu11 nvidia-cublas-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11 cuquantum-cu11

python ./setup.py bdist_wheel -- \
  -DCMAKE_BUILD_TYPE=Release \
  -DAER_MPI=True \
  -DAER_THRUST_BACKEND=CUDA \
  -DAER_CUDA_ARCH=7.0 \
  -DAER_DISABLE_GDR=False \
  -AER_PYTHON_CUDA_ROOT=$install_dir \
  --

pip install --prefix=$install_dir dist/qiskit_aer*.whl
cd -
