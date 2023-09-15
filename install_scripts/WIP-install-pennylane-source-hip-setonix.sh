#!/bin/bash -l
#SBATCH --job-name=install-pennylane-source-hip-setonix
#SBATCH --account=pawsey0001-gpu
#SBATCH --partition=gpu-dev
#SBATCH --exclusive
#SBATCH --ntasks=1
#SBATCH --threads-per-core=1
#SBATCH --gpus-per-node=8
#SBATCH --time=00:30:00
#SBATCH --output=out-%x

. use-pennylane-source-hip-setonix.sh

# install from source
git clone https://github.com/PennyLaneAI/pennylane-lightning-kokkos $source_dir/pennylane-lightning-kokkos
cd $source_dir/pennylane-lightning-kokkos
git checkout v$pl_ver

#CMAKE_ARGS="-DCMAKE_CXX_COMPILER=hipcc \
#  -DCMAKE_BUILD_TYPE=Release \
#  -DKokkos_ENABLE_HIP=ON \
#  -DKokkos_ARCH_VEGA90A=ON \
#  -DPLKOKKOS_ENABLE_NATIVE=ON" \
#  pip install --prefix=$install_dir .

rm -fr build PennyLane_Lightning_Kokkos.egg-info
cmake -B build . \
  -DCMAKE_CXX_COMPILER=hipcc \
  -DCMAKE_CXX_FLAGS=--gcc-toolchain=$(dirname $(which g++))/../snos \
  -DCMAKE_BUILD_TYPE=Release \
  -DKokkos_ENABLE_HIP=ON \
  -DKokkos_ARCH_VEGA90A=ON \
  -DPLKOKKOS_ENABLE_NATIVE=ON
#  -DCMAKE_VERBOSE_MAKEFILE=ON \
#  -DPLKOKKOS_ENABLE_WARNINGS=ON \

# Marco's workaround for pybind11 build configuration issue
# (incorrectly picking up system Python instead of module Python)
echo "Patching build/CMakeCache.txt"
sed -i "s;/usr/bin/python3\.6;$PAWSEY_PYTHON_HOME/bin/python$python_ver;g" build/CMakeCache.txt
sed -i "s;/usr/include/python3\.6m;$PAWSEY_PYTHON_HOME/include/python$python_ver;g" build/CMakeCache.txt 
sed -i "s;/usr/lib64/libpython3\.6m\.so;$PAWSEY_PYTHON_HOME/lib/libpython$python_ver.so;g" build/CMakeCache.txt 
sed -i "s;3\.6\.15(3\.6);$py_ver($python_ver);g" build/CMakeCache.txt 
sed -i "s;3\.6\.15;$py_ver;g" build/CMakeCache.txt 
sed -i "s;36m;${python_ver/./};g" build/CMakeCache.txt
echo "Patching build/CMakeFiles/lightning_kokkos_qubit_ops.dir/flags.make"
sed -i "s;/usr/include/python3\.6m;$PAWSEY_PYTHON_HOME/include/python$python_ver;g" build/CMakeFiles/lightning_kokkos_qubit_ops.dir/flags.make

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
