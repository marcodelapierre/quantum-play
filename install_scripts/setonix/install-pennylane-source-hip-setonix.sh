#!/bin/bash -l
#SBATCH --job-name=install-pennylane-source-hip-setonix
#SBATCH --account=pawsey0001-gpu
#SBATCH --partition=gpu-dev
#SBATCH --ntasks=1
#SBATCH --threads-per-core=1
#SBATCH --gpus-per-node=1
#SBATCH --time=00:30:00
#SBATCH --output=out-%x

# essential for reproducibility of installation
# pennylane versions
tool_name="pennylane-hip"
pl_ver="0.32.0"
# host versions
py_ver="3.10.10"
pip_ver="23.1.2-py3.10.10"
st_ver="68.0.0-py3.10.10"
rocm_ver="5.2.3"

# load modules
module load python/$py_ver
module load py-pip/$pip_ver
module load py-setuptools/$st_ver
module load rocm/$rocm_ver
module load craype-accel-amd-gfx90a

# internal variables - do not edit
python_ver="$( python3 -V | cut -d ' ' -f 2 | cut -d . -f 1,2 )"
install_dir="$(pwd)/$tool_name"
source_dir="${install_dir}-src"
lib_dir="$install_dir/lib/python${python_ver}/site-packages"
bin_dir="$install_dir/bin"
#
export PYTHONPATH="$lib_dir:$PYTHONPATH" 
export PATH="$bin_dir:$PATH"

# install from source
git clone https://github.com/PennyLaneAI/pennylane-lightning-kokkos $source_dir/pennylane-lightning-kokkos
cd $source_dir/pennylane-lightning-kokkos
git checkout v$pl_ver
sed -i 's;GIT_TAG *3\.7.*;GIT_TAG        4.1.00;g' CMakeLists.txt
rm -fr build PennyLane_Lightning_Kokkos.egg-info

#CMAKE_ARGS="-DCMAKE_CXX_COMPILER=hipcc \
#  -DCMAKE_BUILD_TYPE=Release \
#  -DCMAKE_PREFIX_PATH=$install_dir \
#  -DPLKOKKOS_ENABLE_NATIVE=ON \
#  -DKokkos_ENABLE_HIP=ON \
#  -DKokkos_ARCH_VEGA90A=ON" \
#  pip install --prefix=$install_dir .

cmake -B build . \
  -DCMAKE_CXX_COMPILER=hipcc \
  -DCMAKE_CXX_FLAGS=--gcc-toolchain=$(dirname $(which g++))/../snos \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH=$install_dir \
  -DPLKOKKOS_ENABLE_NATIVE=ON \
  -DKokkos_ENABLE_HIP=ON \
  -DKokkos_ARCH_VEGA90A=ON
#  -DCMAKE_VERBOSE_MAKEFILE=ON \
#  -DPLKOKKOS_ENABLE_WARNINGS=ON \

# Edric's workaround for __noinline__ build issue
# Also requires --gcc-toolchain above
files=$(grep -rl "#include <memory>" build)
for file in $files; do
  echo "Patching $file"
  sed -i 's/#include <memory>/#ifdef __noinline__\
      #define GCC12_RESTORE_NOINLINE\
      #undef __noinline__\
    #endif\
    #include <memory>\
    #ifdef GCC12_RESTORE_NOINLINE\
      #undef GCC12_RESTORE_NOINLINE\
      #define __noinline__ _attribute((noinline))\
    #endif/g' $file
done

cmake --build build
pip install --prefix=$install_dir .
cd -

# configure for startup
echo "export PYTHONPATH=\"$lib_dir:\$PYTHONPATH\"" >> $(eval echo ~${USERID})/.bashrc
echo "export PATH=\"$bin_dir:\$PATH\"" >> $(eval echo ~${USERID})/.bashrc

