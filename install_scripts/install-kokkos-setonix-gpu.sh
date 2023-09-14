#!/bin/bash -l
#SBATCH --job-name=install-kokkos-setonix-gpu
#SBATCH --account=pawsey0001-gpu
#SBATCH --partition=gpu-dev
#SBATCH --exclusive
#SBATCH --ntasks=1
#SBATCH --threads-per-core=1
#SBATCH --gpus-per-node=8
#SBATCH --time=00:30:00
#SBATCH --output=out-%x

download_kokkos="1"
kokkos_version="3.7.02"
suffix="-setonix-gpu"

module load rocm/5.2.3
module load craype-accel-amd-gfx90a

if [ "$download_kokkos" != "0" ] ; then
 rm -rf kokkos-cpu
 git clone https://github.com/kokkos/kokkos kokkos${suffix}-src
fi

cd kokkos${suffix}-src
git checkout $kokkos_version

mkdir build
cd build

cmake .. \
  -DCMAKE_INSTALL_PREFIX=$(pwd)/../../kokkos$suffix \
  -DCMAKE_CXX_COMPILER=hipcc \
  -DCMAKE_BUILD_TYPE=Release \
  -DKokkos_ENABLE_HIP=On \
  -DKokkos_ARCH_ZEN3=On \
  -DKokkos_ARCH_VEGA90A=On \
  -DKokkos_ENABLE_HIP_MULTIPLE_KERNEL_INSTANTIATIONS=On

make -j $SLURM_CPUS_PER_TASK
sg pawsey0001 -c 'make install'
